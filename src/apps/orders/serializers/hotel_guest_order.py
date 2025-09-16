from django.db import transaction

from rest_framework import serializers

from apps.base.exceptions import CustomExceptionError
from apps.guests.models import Guest
from apps.guests.utils.prepare_guests import prepare_bulk_guests
from apps.orders.models.hotel_order import HotelOrder
from apps.base.serializers import CustomModelSerializer
from apps.guests.serializers.order_guests import GuestListSerializer
from apps.orders.serializers import OnlyFoodOrderSerializer


class HotelOrderGuestSerializer(CustomModelSerializer):
    guests = GuestListSerializer(many=True, read_only=True)
    guest_details = serializers.ListField(write_only=True, child=serializers.DictField())
    guest_group = serializers.UUIDField(write_only=True, required=False)
    order_status = serializers.CharField(read_only=True)
    hotel_name = serializers.CharField(source="hotel.name", read_only=True)
    guest_type = serializers.CharField(read_only=True)
    order_food = OnlyFoodOrderSerializer(source="food_order", read_only=True, many=True)

    class Meta:
        model = HotelOrder
        fields = [
            "id",
            "hotel",
            "hotel_name",
            "order_status",
            "room",
            "guest_type",
            "guests",
            "guest_details",
            "guest_group",
            "order_food",
            "food_order",
            "check_in",
            "check_out",
            "count_of_people",
            "created_at",
            "order_id",
            "general_cost"
        ]
        read_only_fields = ["order_id", "general_cost"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop("food_order")
        data["total_food_price"] = 0
        data["hotel_total_price"] = data.pop("general_cost")
        data["general_cost"] = 0
        for order in data["order_food"]:
            data["total_food_price"] += order["total_price"]
            data["general_cost"] += order["total_price"]
        data["general_cost"] += data["hotel_total_price"]
        return data

    def validate(self, data):
        count_of_people = data.get("count_of_people", 0)
        guests_data = data.get("guest_details", [])
        guest_group = data.get("guest_group", None)

        if guest_group and guests_data:
            raise CustomExceptionError(
                code=400,
                detail="Iltimos, yoki `guest_group`, yoki `guest_details` dan birini kiriting — ikkalasi birga bo‘lmaydi.")

        if not guest_group and not guests_data:
            raise CustomExceptionError(
                code=400,
                detail="Iltimos, `guest_group` yoki `guest_details` dan birini kiriting.")

        if guests_data and count_of_people != len(guests_data):
            raise CustomExceptionError(code=400, detail="Mehmonlar soni kiritilgan odamlar soniga teng bo‘lishi kerak.")

        return data

    def create(self, validated_data):
        guests_data = validated_data.pop("guest_details", [])
        guest_group = validated_data.pop("guest_group", None)
        food_orders = validated_data.pop("food_order", [])

        with transaction.atomic():
            hotel_order = HotelOrder.objects.create(**validated_data)
            hotel_order.food_order.set(food_orders)

            if guests_data:
                guests = prepare_bulk_guests(
                    hotel=hotel_order.hotel,
                    room=hotel_order.room,
                    guests_data=guests_data,
                    check_in=hotel_order.check_in,
                    check_out=hotel_order.check_out
                )
                Guest.objects.bulk_create(guests)
                hotel_order.guests.set(guests)

            elif guest_group:
                hotel_order.guest_group_id = guest_group
                hotel_order.save(update_fields=["guest_group"])

            hotel_order.calculate_prices()
            hotel_order.save(update_fields=["general_cost"])

            if hotel_order.guest_type == HotelOrder.GuestType.INDIVIDUAL and hotel_order.room:
                hotel_order.room.refresh_occupancy()
            elif hotel_order.guest_type == HotelOrder.GuestType.GROUP:
                for room in hotel_order.rooms.all():
                    room.refresh_occupancy()

        return hotel_order


{
    "hotel": "ee3c774a-705e-4689-add4-2424d58a40cf",
    "order_status": "Planned",
    "room": "7894f1bd-27ef-4421-91eb-e5ee2d134b3e",
    "guest_details": [
        {"full_name": "Franko", "gender": 1},
        {"full_name": "Victus", "gender": 1}
    ],
    "check_in": "22.09.2025 15:50",
    "check_out": "25.09.2025 15:50",
    "count_of_people": 2
}

{
    "hotel": "37e482df-9319-435f-afc8-d2f5adb4d19e",
    "order_status": "Planned",
    "room": "fcd4bfa7-fbac-47d6-a93f-8fce844f3238",
    "guest_group": "97893ec0-3345-4130-a801-e3d05735feba",
    "check_in": "22.07.2025 15:50",
    "check_out": "25.07.2025 15:50",
    "count_of_people": 2
}
