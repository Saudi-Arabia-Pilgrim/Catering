from django.db import transaction

from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.guests.models import Guest
from apps.guests.serializers.order_guests import GuestForHotelOrderSerializer
from apps.orders.models.hotel_order import HotelOrder


class HotelOrderGuestSerializer(CustomModelSerializer):
    guests = GuestForHotelOrderSerializer(many=True, read_only=True)
    guest_details = serializers.ListField(write_only=True, child=serializers.DictField())

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
            raise serializers.ValidationError("Mehmonlar soni kiritilgan odamlar soniga teng bo‘lishi kerak.")

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


# {
#     "hotel": "c3776dbb-09ee-4b37-8d51-342c7dacae08",
#     "order_status": "Active",
#     "room": "4940017b-9f46-47a3-9ca4-1928c3967a45",
#     "guest_details": [
#     {"full_name": "Alkash", "gender": 2},
#     {"full_name": "Bo`mish", "gender": 2}
# ],
#     "check_in": "22.03.2025 15:50",
#     "check_out": "28.03.2025 15:50",
#     "count_of_people": 2
# }
