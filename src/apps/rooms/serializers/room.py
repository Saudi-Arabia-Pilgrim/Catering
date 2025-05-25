from celery.app.trace import send_postrun
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
    room_name = serializers.CharField()
    hotel_name = serializers.CharField()
    room_type = serializers.UUIDField()
    hotel = serializers.UUIDField()
    gross_price = serializers.DecimalField(max_digits=15, decimal_places=2)
    count = serializers.IntegerField()
    occupied_count = serializers.IntegerField()
    available_count = serializers.IntegerField()
    remaining_capacity = serializers.IntegerField()


    class Meta:
        model = Room
        fields = [
            "room_type",
            "room_name",
            "hotel",
            "hotel_name",
            "count",
            "occupied_count",
            "available_count",
            "remaining_capacity",
            "gross_price",
        ]
        read_only_fields = ["room_name", "hotel_name"]


class RoomCreateSerializer(CustomModelSerializer):
    count = serializers.IntegerField(min_value=1, write_only=True)
    room_name = serializers.CharField(source="room_type.name", read_only=True)

    class Meta:
        model = Room
        fields = [
            "id",
            "hotel",
            "room_type",
            "room_name",
            "count",
            "capacity",
            "net_price",
            "profit",
        ]
        read_only_fields = ["room_name"]

    def validate(self, attrs):
        attrs["net_price"] = attrs.get("net_price") or 0
        attrs["profit"] = attrs.get("profit") or 0
        attrs["gross_price"] = attrs["net_price"] + attrs["profit"]

        return attrs

    def create(self, validated_data):
        counts = validated_data.pop("count")
        room_list = []

        for count in range(counts):
            room_list.append(Room(
                hotel=validated_data["hotel"],
                room_type=validated_data["room_type"],
                capacity=validated_data["capacity"],
                count=1,
                available_count=1,
                occupied_count=0,
                net_price=validated_data["net_price"],
                profit=validated_data["profit"],
                gross_price=validated_data["gross_price"]
            ))
        Room.objects.bulk_create(room_list)
        return room_list

{
    "hotel": "5387b602-0025-4cec-9efa-76f6288bfb74",
    "order_status": "Active",
    "room": "2f07bae8-2693-4ee5-9237-f5013c65e025",
    "guest_details": [
    {"full_name": "Leyla", "gender": 2},
    {"full_name": "Gossen", "gender": 1},
],
    "check_in": "25.05.2025 15:50",
    "check_out": "29.05.2025 15:50",
    "count_of_people": 2
}