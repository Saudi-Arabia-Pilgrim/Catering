from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.counter_agents.serializers import CounterAgentSerializer
from apps.orders.models import FoodOrder
from apps.foods.serializers import FoodSerializerForFoodOrder
from apps.menus.serializers import MenuSerializer, RecipeSerializer


class OnlyFoodOrderSerializer(CustomModelSerializer):
    total_price = serializers.SerializerMethodField(read_only=True)
    product_type = serializers.SerializerMethodField(read_only=True)
    order_type = serializers.SerializerMethodField(read_only=True)
    experience_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FoodOrder
        fields = [
            "id",
            "food_order_id",
            "food",
            "menu",
            "recipe",
            "product_type",
            "product_count",
            "order_type",
            "order_time",
            "experience_date",
            "counter_agent",
            "address",
            "price",
            "status",
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

    def get_order_type(self, obj):
        return obj.get_product_type_display()

    def get_product_type(self, obj):
        return obj.get_order_type_display()
    
    def get_experience_date(self, obj):
        return obj.experience_date_str


class FoodOrderRetrieveSerializer(OnlyFoodOrderSerializer):
    food = FoodSerializerForFoodOrder(read_only=True)
    menu = MenuSerializer(read_only=True)
    recipe = RecipeSerializer(read_only=True)
    counter_agent = CounterAgentSerializer(read_only=True)

    class Meta(OnlyFoodOrderSerializer.Meta):
        pass