from django.db import transaction

from rest_framework import serializers

from apps.base.exceptions import CustomExceptionError
from apps.guests.models import Guest
from apps.orders.models.hotel_order import HotelOrder
from apps.base.serializers import CustomModelSerializer
from apps.guests.serializers.order_guests import GuestListSerializer
from apps.orders.serializers import OnlyFoodOrderSerializer


class HotelOrderGuestSerializer(CustomModelSerializer):
    guests = GuestListSerializer(many=True, read_only=True)
    guest_details = serializers.ListField(write_only=True, child=serializers.DictField())
    order_status = serializers.ChoiceField(choices=HotelOrder.OrderStatus.choices, required=False)
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
        """HotelOrder yaratish va mehmonlarni qo‘shish"""
        guests_data = validated_data.pop("guest_details")
        food_orders = validated_data.pop("food_order")

        with transaction.atomic():
            hotel_order = HotelOrder.objects.create(**validated_data)
            hotel_order.food_order.set(food_orders)
            guests = []
            for guest_data in guests_data:
                guest = Guest.objects.create(
                    hotel=hotel_order.hotel,
                    room=hotel_order.room,
                    full_name=guest_data["full_name"],
                    gender=guest_data["gender"],
                    check_in=hotel_order.check_in,
                    check_out=hotel_order.check_out
                )
                guests.append(guest)
            hotel_order.guests.set(guests)

        return hotel_order


{
    "hotel": "83f17927-513e-485f-b2b2-5bfd38dd7a7d",
    "order_status": "Active",
    "room": "4a89b391-f23c-4e55-a521-35aadd8c31b4",
    "guest_details": [
    {"full_name": "Victus", "gender": 1}
],
    "food_order": ["4d72f09e-acf8-40ca-b719-e89d3886d1a6"],
    "check_in": "1.06.2025 14:50",
    "check_out": "8.06.2025 14:50",
    "count_of_people": 1
}