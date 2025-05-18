from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.guests.models import Guest
from apps.guests.serializers import ActiveNoGuestListSerializer
from apps.orders.models import HotelOrder
from apps.base.serializers import CustomModelSerializer
from apps.orders.serializers import OnlyFoodOrderSerializer
from apps.rooms.models import Room, RoomType
from apps.warehouses.utils import validate_uuid


class NoActiveHotelOrderFoodSerializer(CustomModelSerializer):
    guests = serializers.SerializerMethodField(read_only=True)
    food_order = OnlyFoodOrderSerializer(many=True, read_only=True)
    nights = serializers.SerializerMethodField()
    total_guest_cost = serializers.SerializerMethodField()
    total_food_cost = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = HotelOrder
        fields = [
            "order_id",
            "hotel",
            "room",
            "order_status",
            "check_in",
            "check_out",
            "nights",
            "count_of_people",
            "guests",
            "food_order",
            "total_guest_cost",
            "total_food_cost",
            "total_cost",
            "created_at",
        ]
        read_only_fields = ["created_at", "total_cost"]

    def get_guests(self, obj):
        request = self.context.get("request")
        if not request:
            return ActiveNoGuestListSerializer(obj.hotel.guests.all(), many=True).data
        room_type_id = request.GET.get("room_type")
        if not room_type_id:
            return ActiveNoGuestListSerializer(obj.hotel.guests.all(), many=True).data
        validate_uuid(room_type_id)
        room_type = get_object_or_404(RoomType, pk=room_type_id)
        rooms = Room.objects.filter(room_type=room_type)
        guests = Guest.objects.filter(room__in=rooms)
        return ActiveNoGuestListSerializer(guests, many=True).data

    def get_nights(self, obj):
        return (obj.check_out - obj.check_in).days

    def get_total_guest_cost(self, obj):
        total = sum([guest.price for guest in obj.guests.all()])
        return total

    def get_total_food_cost(self, obj):
        total = sum([f.total_price for f in obj.food_order.all()])
        return total

    def get_total_cost(self, obj):
        return self.get_total_guest_cost(obj) + self.get_total_food_cost(obj)