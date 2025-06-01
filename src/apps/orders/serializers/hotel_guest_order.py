from django.db import transaction

from rest_framework import serializers

from apps.base.exceptions import CustomExceptionError
from apps.guests.models import Guest
from apps.orders.models.hotel_order import HotelOrder
from apps.base.serializers import CustomModelSerializer
from apps.guests.serializers.order_guests import GuestListSerializer


class HotelOrderGuestSerializer(CustomModelSerializer):
    guests = GuestListSerializer(many=True, read_only=True)
    guest_details = serializers.ListField(write_only=True, child=serializers.DictField())
    order_status = serializers.ChoiceField(choices=HotelOrder.OrderStatus.choices, required=False)
    hotel_name = serializers.CharField(source="hotel.name", read_only=True)

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
            "check_in",
            "check_out",
            "count_of_people",
            "created_at",
            "order_id",
            "general_cost"
        ]
        read_only_fields = ["order_id", "general_cost"]

    def validate(self, data):
        count_of_people = data.get("count_of_people", 0)
        guests_data = data.get("guest_details", [])

        if count_of_people != len(guests_data):
            raise CustomExceptionError(code=404, detail="Mehmonlar soni kiritilgan odamlar soniga teng bo‘lishi kerak.")

        return data

    def create(self, validated_data):
        """HotelOrder yaratish va mehmonlarni qo‘shish"""
        guests_data = validated_data.pop("guest_details")

        with transaction.atomic():
            hotel_order = HotelOrder.objects.create(**validated_data)
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
    "hotel": "cae10738-d67d-4b79-bd1a-c2f94f0fd2dc",
    "order_status": "Active",
    "room": "faf28841-29df-4a3e-b2de-bb9667562f10",
    "guest_details": [
    {"full_name": "Julian", "gender": 1}
],
    "check_in": "1.06.2025 03:00",
    "check_out": "7.06.2025 03:00",
    "count_of_people": 1
}