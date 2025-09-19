from django.db import transaction

from rest_framework import serializers

from apps.orders.utils.calculate_price import calculate_prices_for_order
from apps.rooms.models import Room
from apps.guests.models import Guest, GuestGroup
from apps.base.exceptions import CustomExceptionError
from apps.orders.models.hotel_order import HotelOrder
from apps.base.serializers import CustomModelSerializer
from apps.orders.serializers import OnlyFoodOrderSerializer
from apps.guests.utils.prepare_guests import prepare_bulk_guests
from apps.guests.serializers.order_guests import GuestListSerializer


class HotelOrderGuestSerializer(CustomModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), required=False)
    guests = GuestListSerializer(many=True, read_only=True)
    guest_details = serializers.ListField(write_only=True, child=serializers.DictField(), required=False)
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
            "rooms",
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

        if instance.guest_group:
            data["guest_group"] = {
                "id": str(instance.guest_group.id),
                "name": instance.guest_group.name,
                "count": instance.guest_group.count,
                "guest_group_status": instance.guest_group.guest_group_status,
            }

        else:
            data["guest_group"] = None

        return data

    def validate(self, data):
        guests_data = data.get("guest_details")
        guest_group = data.get("guest_group")
        rooms = data.get("rooms")
        room = data.get("room")

        if guest_group and guests_data:
            raise CustomExceptionError(code=400, detail="Faqat bittasi: guest_group yoki guest_details")

        if not guest_group and not guests_data:
            raise CustomExceptionError(code=400, detail="guest_group yoki guest_details kerak")

        if guests_data and not room:
            raise CustomExceptionError(code=400, detail="Individual order uchun room shart")

        if guest_group and not rooms:
            raise CustomExceptionError(code=400, detail="Group order uchun rooms kerak")

        if guests_data and data.get("count_of_people") != len(guests_data):
            raise CustomExceptionError(code=400, detail="guest_details bilan count_of_people mos emas")

        return data

    def create(self, validated_data):
        guests_data = validated_data.pop("guest_details", [])
        guest_group_id = validated_data.pop("guest_group", None)
        rooms = validated_data.pop("rooms", [])
        food_orders = validated_data.pop("food_order", [])

        validated_data["guest_type"] = (
            HotelOrder.GuestType.GROUP if guest_group_id else HotelOrder.GuestType.INDIVIDUAL
        )

        with transaction.atomic():
            order = HotelOrder.objects.create(**validated_data)
            order.food_order.set(food_orders)

            if guests_data:
                guests = prepare_bulk_guests(
                    hotel=order.hotel,
                    room=order.room,
                    guests_data=guests_data,
                    check_in=order.check_in,
                    check_out=order.check_out
                )
                Guest.objects.bulk_create(guests)
                order.guests.set(guests)

            # Group guest order (ko‘p room, 1 ta guest_group)
            elif guest_group_id:
                order.guest_group_id = guest_group_id
                order.save(update_fields=["guest_group"])
                order.rooms.set(rooms)

                guest_group = GuestGroup.objects.get(id=guest_group_id)
                guest_group.guest_group_status = GuestGroup.GuestGroupStatus.ACCEPTED
                guest_group.save(update_fields=["guest_group_status"])

            # Har doim narxni hisoblash
            calculate_prices_for_order(order)
            order.save(update_fields=["general_cost"])

            # Faqat kerakli room'lar uchun occupancy ni yangilash
            rooms_to_refresh = [
                order.room] if order.guest_type == HotelOrder.GuestType.INDIVIDUAL else order.rooms.all()
            for room in rooms_to_refresh:
                room.refresh_occupancy()

        return order


{
    "hotel": "31b1954a-fe25-45f1-9a41-f31b5bcd7186",
    "order_status": "Planned",
    "room": "3e8a7343-c62c-4569-b8aa-b3190ab59bf5",
    "guest_details": [
        {"full_name": "Franko", "gender": 1}
    ],
    "check_in": "18.09.2025 15:50",
    "check_out": "25.09.2025 15:50",
    "count_of_people": 1
}

{
    "hotel": "31b1954a-fe25-45f1-9a41-f31b5bcd7186",
    "order_status": "Active",
    "rooms": [
     "8f66f215-6e94-4137-adbc-b26a556b63ee",
     "8cbdf875-530f-4f05-966e-6bb04bc3368f",
     "e3cb2b84-047f-4e2f-b233-f8f0662c9cf9",
     "6cb674da-4929-47c7-95c8-aa6a6f9fc07c",
     "896a2cf0-b366-4c2d-b3f7-16ab9ed62829"
],
    "guest_group": "f08a0375-452c-4134-a8ad-c680dce608ac",
    "check_in": "18.07.2025 15:50",
    "check_out": "25.07.2025 15:50",
    "count_of_people": 10
}
