from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.orders.models import FoodOrder


class FoodOrderSerializer(CustomModelSerializer):

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = FoodOrder
        fields = [
            "food_order_id",
            "hotel_order",
            "expiration_date",
            "order_type",
            "product_type",
            "price",
            "address",
            "product_count",
            "total_price",
            "created_at"
        ]

    def get_total_price(self, obj):
        return obj.total_price