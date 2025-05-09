from django.db import models

from rest_framework import serializers

from apps.guests.serializers.order_guests import GuestListSerializer
from apps.hotels.models import Hotel
from apps.base.serializers import CustomModelSerializer
from apps.rooms.serializers import RoomSerializer


class HotelSerializer(CustomModelSerializer):
    """
    Serializer for the Hotel model.

    This serializer includes hotel details along with related rooms and guests.
    """

    rooms = RoomSerializer(many=True, help_text="List of rooms associated with the hotel.", read_only=True)
    guests = GuestListSerializer(many=True, read_only=True)

    total_guests_price = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = [
            "id",
            "name",
            "address",
            "email",
            "phone_number",
            "rating",
            "rooms",
            "guests",
            "total_guests_price"
        ]
        help_texts = {
            "id": "Unique identifier for the hotel.",
            "name": "The name of the hotel.",
            "address": "The physical address of the hotel.",
            "email": "Contact email of the hotel.",
            "phone_number": "Contact phone number of the hotel.",
            "rating": "Hotel rating (0.00 - 5.00).",
        }

    def get_total_guests_price(self, obj):
        return obj.guests.aggregate(total=models.Sum("price"))["total"] or 0
