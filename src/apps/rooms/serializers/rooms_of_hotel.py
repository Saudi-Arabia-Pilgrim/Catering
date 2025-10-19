from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.rooms.models import Room


class RoomsOfHotelListSerializer(CustomModelSerializer):
    room_name = serializers.CharField(source="room_type.name")
    hotel_name = serializers.CharField(source="hotel.name")

    class Meta:
        model = Room
        fields = [
            "id",
            "hotel",
            "hotel_name",
            "room_type",
            "room_name",
            "floor",
            "room_number",
            "is_busy",
            "available_count",
            "occupied_count",
            "remaining_capacity",
            "capacity",
            "gross_price"
        ]