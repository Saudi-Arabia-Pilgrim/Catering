from rest_framework import serializers

from apps.orders.models import FoodOrder
from apps.base.serializers import CustomModelSerializer


class OrderFoodSerializer(CustomModelSerializer):
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FoodOrder
        fields = [
            "id",
            "food_order_id",
            "menu",
            "product_count",
            "total_price",
            "created_at",
        ]

        read_only_fields = [
            "status",
            "id",
            "food_order_id",
            "total_price",
            "price",
            "order_type",
            "product_type",
        ]

    def get_total_price(self, obj):
        return obj.total_price