from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.rooms.models.rooms import Room


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
            "room",
            "capacity",
            "status",
            "count",
            "occupied_count",
            "available_count",
            "net_price",
            "profit",
            "gross_price"
        ]

    def get_available_count(self, obj):
        """
        Calculates the number of available rooms.

        Args:
            obj (Room): The Room instance.

        Returns:
            int: The number of available rooms.
        """
        return obj.available_count


class RoomBookedSerializer(CustomModelSerializer):
    """
    Serializer for the RoomType model with available and booked counts.
    """
    available_count = serializers.SerializerMethodField()
    booked_count = serializers.SerializerMethodField()

    room_type = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            "room_type",
            "available_count",
            "booked_count",
            "price",
        ]

    def get_room_type(self, obj):
        return obj.room_type.name

    def get_available_count(self, obj):
        """
        Return the number of available (not booked) rooms for this room type.
        """
        return obj.count - obj.occupied_count

    def get_booked_count(self, obj):
        """
        Return the number of booked rooms for this room type.
        """
        return obj.occupied_count