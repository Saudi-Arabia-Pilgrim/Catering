from rest_framework import serializers

from apps.base.exceptions import CustomExceptionError
from apps.base.serializers import CustomModelSerializer
from apps.counter_agents.models import CounterAgent
from apps.menus.serializers import MenuSerializer
from apps.orders.models import FoodOrder


class CounterAgentSerializer(CustomModelSerializer):
    class Meta:
        model = CounterAgent
        fields = [
            "id",
            "order_type",
            "name",
            "address",
            "status",
        ]


class OnlyFoodOrderSerializer(CustomModelSerializer):
    counter_agent = serializers.PrimaryKeyRelatedField(queryset=CounterAgent.objects.all())
    total_price = serializers.SerializerMethodField()
    menu = MenuSerializer(many=True)

    class Meta:
        model = FoodOrder
        fields = [
            "food_order_id",
            "counter_agent",
            "menu",
            "food",
            "order_type",
            "order_time",
            "expiration_date",
            "product_type",
            "address",
            "product_count",
            "price",
            "total_price",
            "created_at"
        ]
        read_only_fields = ["food_order_id", "total_price"]

    def validate(self, attrs):
        food = self.instance.food if self.instance else None
        menu = self.instance.menu if self.instance else None
        recipe = self.instance.recipe if self.instance else None

        if bool(attrs.get("food", food)) + bool(attrs.get("menu", menu)) + bool(attrs.get("recipe", recipe)) != 1:
            raise CustomExceptionError(code=400, detail="Only one of 'food', 'menu', or 'recipe' must be set.")
        return attrs

    def get_total_price(self, obj):
        return obj.total_price