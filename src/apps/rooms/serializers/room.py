from rest_framework import serializers

from apps.rooms.models.rooms import Room
from apps.base.serializers import CustomModelSerializer


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
    room_name = serializers.CharField(source="room_type.name", read_only=True)
    capacity = serializers.IntegerField(required=False, allow_null=True, read_only=True)
    hotel_name = serializers.CharField(source="hotel.name", read_only=True)

    class Meta:
        model = Room
        fields = [
            "id",
            "hotel",
            "hotel_name",
            "room_type",
            "room_name",
            "count",
            "capacity",
            "net_price",
            "profit",
            "gross_price"
        ]
        read_only_fields = ["room_name", "capacity", "hotel_name"]


class RoomBookedSerializer(CustomModelSerializer):
    """
    Serializer for the RoomType model with available and booked counts.
    """
    available_count = serializers.SerializerMethodField()
    booked_count = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            "room_type",
            "available_count",
            "booked_count",
            "price",
        ]

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