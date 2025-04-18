from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.guests.models import Guest
from apps.hotels.models import Hotel


class GuestForHotelOrderSerializer(CustomModelSerializer):
    """
    Serializer for the Guest model.

    This serializer handles guest-related data, including retrieving guest details
    and creating new guest entries with an associated hotel.
    """
    room_type = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Guest
        fields = [
            "id",
            "full_name",
            "order_number",
            "room",
            "room_type",
            "gender",
            "check_in",
            "check_out",
            "total_price"
        ]
        read_only_fields = ["order_number", "price", "room_type"]

    def get_room_type(self, obj):
        if hasattr(obj, 'room') and hasattr(obj.room, 'room_type'):
            return obj.room.room_type.name
        return obj.room.room_type.name if obj.room_id else None

    def get_total_price(self, obj):
        if obj.check_in and obj.check_out and obj.room:
            days_stayed = (obj.check_out - obj.check_in).days
            if days_stayed < 1:
                days_stayed = 1
            return obj.room.gross_price * days_stayed
        return 0




