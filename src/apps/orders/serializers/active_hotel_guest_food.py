from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.guests.models import Guest
from apps.guests.serializers.group_guests import GuestGroupListSerializer
from apps.orders.models import FoodOrder
from apps.orders.models.hotel_order import HotelOrder
from apps.guests.serializers import ActiveNoGuestListSerializer
from apps.orders.serializers import OnlyFoodOrderSerializer
from apps.rooms.models import RoomType, Room
from apps.warehouses.utils import validate_uuid


class ActiveHotelOrderFoodSerializer(CustomModelSerializer):
    hotel_name = serializers.CharField(source="hotel.name")
    guests = serializers.SerializerMethodField(read_only=True)
    food_order = OnlyFoodOrderSerializer(many=True, read_only=True)
    guest_group = GuestGroupListSerializer(read_only=True)
    nights = serializers.SerializerMethodField()
    total_guest_cost = serializers.SerializerMethodField()
    total_food_cost = serializers.SerializerMethodField()
    general_cost = serializers.SerializerMethodField()

    class Meta:
        model = HotelOrder
        fields = [
            "id",
            "order_id",
            "hotel",
            "hotel_name",
            "room",  # individual guests uchun asosiy xona
            "rooms",  # group guests uchun ko‘p xonalar
            "food_service",
            "guest_group",  # group guests holati uchun group info
            "order_status",
            "check_in",
            "check_out",
            "nights",
            "count_of_people",
            "guests",
            "food_order",
            "total_guest_cost",
            "total_food_cost",
            "general_cost",
            "created_at",
        ]
        read_only_fields = ["created_at", "total_cost"]

    def get_guests(self, obj):
        request = self.context.get("request")
        if not request:
            return ActiveNoGuestListSerializer(obj.guests.all(), many=True).data

        room_type_id = request.GET.get("room_type")
        if not room_type_id:
            return ActiveNoGuestListSerializer(obj.guests.all(), many=True).data

        validate_uuid(room_type_id)
        room_type = get_object_or_404(RoomType, pk=room_type_id)
        rooms = Room.objects.filter(room_type=room_type)
        guests = Guest.objects.filter(room__in=rooms)
        return ActiveNoGuestListSerializer(guests, many=True).data

    def get_nights(self, obj):
        return (obj.check_out - obj.check_in).days

    def get_total_guest_cost(self, obj):
        return sum([guest.price for guest in obj.guests.all()])

    def get_total_food_cost(self, obj):
        return sum([f.total_price for f in obj.food_order.all()])

    def get_general_cost(self, obj):
        return self.get_total_guest_cost(obj) + self.get_total_food_cost(obj)


class HotelOrderCreateSerializer(serializers.ModelSerializer):
    food_order = serializers.PrimaryKeyRelatedField(
        queryset=FoodOrder.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = HotelOrder
        fields = [
            "order_id",
            "hotel",
            "room",
            "order_status",
            "check_in",
            "check_out",
            "count_of_people",
            "food_order",
        ]

    def create(self, validated_data):
        food_orders = validated_data.pop('food_order', [])
        hotel_order = HotelOrder.objects.create(**validated_data)
        if food_orders:
            hotel_order.food_order.set(food_orders)
        return hotel_order