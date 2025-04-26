from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.orders.models import FoodOrder
from apps.orders.models.hotel_order import HotelOrder
from apps.guests.serializers import GuestListSerializer
from apps.orders.serializers import OnlyFoodOrderSerializer


class ActiveHotelOrderFoodSerializer(CustomModelSerializer):
    guests = GuestListSerializer(many=True, read_only=True)
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
            "food_order",  # input qila oladigan qilib qo‘shildi
        ]

    def create(self, validated_data):
        food_orders = validated_data.pop('food_order', [])
        hotel_order = HotelOrder.objects.create(**validated_data)
        if food_orders:
            hotel_order.food_order.set(food_orders)  # yoki .add(*food_orders)
        return hotel_order