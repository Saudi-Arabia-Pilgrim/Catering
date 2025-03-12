from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.rooms.models.rooms import Room
from apps.rooms.serializers.room_type import RoomTypeSerializer


class RoomSerializer(CustomModelSerializer):
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

    available_count = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            "id",
            "hotel",
            "room_type",
            "count",
            "occupied_count",
            "available_count",
            "price",
        ]

    def get_hotel(self, obj):
        return obj.hotel.name

    def get_room_type(self, obj):
        return obj.room_type.name

    def get_available_count(self, obj):
        """
        Calculates the number of available rooms.

        Args:
            obj (Room): The Room instance.

        Returns:
            int: The number of available rooms.
        """
        return obj.available_count
