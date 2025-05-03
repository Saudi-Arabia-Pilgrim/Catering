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
    # guest_status = serializers.ChoiceField(choices=Guest.Status.choices, read_only=True)
    order_status = serializers.ChoiceField(choices=HotelOrder.OrderStatus.choices, required=False)

    class Meta:
        model = HotelOrder
        fields = [
            "id",
            "hotel",
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
    "hotel": "1e11584a-7fea-4b85-9e8b-6b4e7fded8e9",
    "order_status": "Active",
    "room": "2df35b24-0a8a-448a-ad46-f50f4d7aa647",
    "guest_details": [
    {"full_name": "Miya", "gender": 2}
],
    "check_in": "29.04.2025 15:50",
    "check_out": "30.04.2025 15:50",
    "count_of_people": 1
}