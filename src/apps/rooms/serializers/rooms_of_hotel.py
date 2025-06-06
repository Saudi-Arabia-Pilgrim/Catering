from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.rooms.models import Room


class RoomsOfHotelListSerializer(CustomModelSerializer):
    room_name = serializers.CharField(source="room_type.name")
    hotel_name = serializers.CharField(source="hotel.name")
    remaining_capacity = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Room
        fields = [
            "id",
            "hotel",
            "hotel_name",
            "room_type",
            "room_name",
            "is_busy",
            "available_count",
            "occupied_count",
            "remaining_capacity",
            "gross_price"
        ]

    def get_remaining_capacity(self, obj):
        return obj.capacity - obj.guests.count()