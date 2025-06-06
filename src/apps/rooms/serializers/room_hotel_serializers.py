from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.rooms.models import Room


class RoomHotelSerializer(CustomModelSerializer):
    """
    Serializer for the Room model.

    This serializer provides a structured representation of room data, including
    details about the room type, total count, occupied count, availability, and price.

    Attributes:
        room_type (RoomTypeSerializer): Nested serializer representing the type of the room.
         count (int): Total number of rooms of this type in the hotel.
         occupied_count (int): Number of currently occupied rooms.
        available_count (int): Computed field representing the number of available rooms.
         price (Decimal): Price per night for the room type.
    """
    room_name = serializers.CharField(source="room_type.name")

    class Meta:
        model = Room
        fields = [
            "room_type",
            "room_name",
            "hotel",
            "count",
            "occupied_count",
            "available_count",
            "gross_price",
        ]
        read_only_fields = ["room_name", "hotel_name"]
