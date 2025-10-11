from django.db import models
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from apps.guests.models import Guest
from apps.hotels.models import Hotel
from apps.rooms.models import RoomType, Room
from apps.rooms.serializers import RoomHotelSerializer
from apps.base.serializers import CustomModelSerializer
from apps.rooms.utils.room_format import get_grouped_room_data
from apps.guests.serializers.order_guests import GuestListSerializer
from apps.warehouses.utils import validate_uuid


class HotelListSerializer(CustomModelSerializer):
    rooms = serializers.SerializerMethodField()
    _cached_room_data = None  # class-level cache

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
        ]

    def get_rooms(self, obj):
        if HotelListSerializer._cached_room_data is None:
            from apps.rooms.utils.room_format import get_grouped_room_data
            HotelListSerializer._cached_room_data = get_grouped_room_data()

        hotel_id = obj.id
        return [r for r in HotelListSerializer._cached_room_data if r["hotel"] == hotel_id]

    def get_total_guests_price(self, obj):
        return obj.guests.aggregate(total=models.Sum("price"))["total"] or 0


class HotelRetrieveSerializer(CustomModelSerializer):
    """
    Serializer for the Hotel model.

    This serializer includes hotel details along with related rooms and guests.
    """

    rooms = serializers.SerializerMethodField(help_text="List of rooms associated with the hotel.", read_only=True)
    guests = serializers.SerializerMethodField(read_only=True)

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

    def get_rooms(self, obj):
        return get_grouped_room_data()

    def get_guests(self, obj):
        request = self.context.get("request")
        if not request:
            return GuestListSerializer(obj.guests.all(), many=True).data
        room_type_id = request.GET.get("room_type")
        if not room_type_id:
            return GuestListSerializer(obj.guests.all(), many=True).data
        validate_uuid(room_type_id)
        room_type = get_object_or_404(RoomType, pk=room_type_id)
        rooms = Room.objects.filter(room_type=room_type)
        guests = Guest.objects.filter(room__in=rooms)
        return GuestListSerializer(guests, many=True).data

    def get_total_guests_price(self, obj):
        return obj.guests.aggregate(total=models.Sum("price"))["total"] or 0


class HotelSerializer(CustomModelSerializer):
    """
    Serializer for the Hotel model.

    This serializer includes hotel details along with related rooms and guests.
    """

    rooms = RoomHotelSerializer(many=True, help_text="List of rooms associated with the hotel.", read_only=True)
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
