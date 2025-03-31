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
    order_status = serializers.ChoiceField(HotelOrder.OrderStatus.choices, required=False)

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
            "created_at"
        ]
        read_only_fields = ["order_id", "general_cost"]

    def validate(self, data):
        count_of_people = data["count_of_people"]
        guests_data = data.get("guest_details", [])

        if len(guests_data) != count_of_people:
            raise serializers.ValidationError("Number of guests must match the number of people specified.")

        return data

    def create(self, validated_data):
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
#     "hotel": "1203f8fd-4c8e-4e2c-9052-af0fb28194c9",
#     "order_status": "Active",
#     "room": "5d2cd12b-404a-4c34-a292-1647c2bb927b",
#     "guest_details": [
#       {"full_name": "John Doe", "gender": 1},
#       {"full_name": "Alex Hakson", "gender": 1},
#       {"full_name": "John Hetson", "gender": 1},
#       {"full_name": "Genry Morgan", "gender": 1}
# ],
#     "check_in": "25.04.2025 14:50",
#     "check_out": "30.04.2025 14:50",
#     "count_of_people": 4
# }

