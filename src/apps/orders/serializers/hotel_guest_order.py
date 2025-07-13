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
    order_status = serializers.CharField(read_only=True)
    hotel_name = serializers.CharField(source="hotel.name", read_only=True)
    order_food = OnlyFoodOrderSerializer(source="food_order", read_only=True, many=True)

    class Meta:
        model = HotelOrder
        fields = [
            "id",
            "hotel",
            "hotel_name",
            "order_status",
            "room",
            "guests",
            "guest_details",
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

        if count_of_people != len(guests_data):
            raise CustomExceptionError(code=404, detail="Mehmonlar soni kiritilgan odamlar soniga teng bo‘lishi kerak.")

        return data

    def create(self, validated_data):
        guests_data = validated_data.pop("guest_details")
        # food_orders = validated_data.pop("food_order")

        with transaction.atomic():
            hotel_order = HotelOrder.objects.create(**validated_data)
            # hotel_order.food_order.set(food_orders)

            guests = prepare_bulk_guests(
                hotel=hotel_order.hotel,
                room=hotel_order.room,
                guests_data=guests_data,
                check_in=hotel_order.check_in,
                check_out=hotel_order.check_out
            )

            Guest.objects.bulk_create(guests)
            hotel_order.guests.set(guests)

            hotel_order.room.refresh_occupancy()

        return hotel_order

{
    "hotel": "37e482df-9319-435f-afc8-d2f5adb4d19e",
    "order_status": "Planned",
    "room": "fcd4bfa7-fbac-47d6-a93f-8fce844f3238",
    "guest_details": [
    {"full_name": "Franko", "gender": 1},
    {"full_name": "Victus", "gender": 1}
],
    "check_in": "22.07.2025 15:50",
    "check_out": "25.07.2025 15:50",
    "count_of_people": 2
}