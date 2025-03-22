from django.db import transaction

from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.guests.models import Guest
from apps.guests.serializers.order_guests import GuestForHotelOrderSerializer
from apps.orders.models.hotel_order import HotelOrder
from apps.rooms.serializers import RoomHotelSerializer


class HotelOrderGuestSerializer(CustomModelSerializer):
    guests = GuestForHotelOrderSerializer(many=True, read_only=True)
    guest_details = serializers.ListField(write_only=True, child=serializers.DictField())
    room = RoomHotelSerializer(read_only=True)

    class Meta:
        model = HotelOrder
        fields = [
            "id",
            "hotel",
            "room",
            "guests",
            "guest_details",
            "check_in",
            "check_out",
            "created_at"
        ]
        read_only_fields = ["order_id", "general_cost", "hotel_name"]

    def validate(self, data):
        count_of_people = data["count_of_people"]
        guests_data = data.get("guests", [])

        if len(guests_data) != count_of_people:
            raise serializers.ValidationError("Number of guests must match the number of people specified.")

        return data

    def create(self, validated_data):
        guests_data = validated_data.pop("guests")
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
#     "hotel": "366ee93e-3ee9-41f2-b818-afd41cae4c41",
#     "room": "f20d201d-a902-4dfe-a96a-9ec11363b137",
#     "guests": [
#         {"full_name": "John Doe", "gender": 1},
#         {"full_name": "Alex Hakson", "gender": 1}
#     ],
#     "order_status": "Active",
#     "food_service": false,
#     "check_in": "20.03.2025 14:30",
#     "check_out": "28.03.2025 15:30",
#     "count_of_people": 2
# }

