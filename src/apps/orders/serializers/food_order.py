from rest_framework import serializers

from apps.base.exceptions import CustomExceptionError
from apps.base.serializers import CustomModelSerializer
from apps.orders.models import FoodOrder


class OnlyFoodOrderSerializer(CustomModelSerializer):
    total_price = serializers.SerializerMethodField(read_only=True)
    product_type = serializers.SerializerMethodField(read_only=True)
    order_type = serializers.SerializerMethodField(read_only=True)
    experience_date = serializers.SerializerMethodField(read_only=True)
    counter_agent_name = serializers.CharField(source="counter_agent.name", read_only=True)

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
            "counter_agent_name",
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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["status"] = instance.get_status_display()
        products = ["food", "menu", "recipe"]
        for product in products:
            obj = getattr(instance, product, None)
            if obj:
                data[f"{product}_name"] = obj.name
                break
        return data


class FoodOrderRetrieveSerializer(CustomModelSerializer):
    total_price = serializers.SerializerMethodField(read_only=True)
    product_type = serializers.SerializerMethodField(read_only=True)
    order_type = serializers.SerializerMethodField(read_only=True)
    experience_date = serializers.SerializerMethodField(read_only=True)
    counter_agent_name = serializers.CharField(source="counter_agent.name", read_only=True)

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
            "counter_agent_name",
            "address",
            "price",
            "status",
            "total_price",
            "created_at",
        ]

        read_only_fields = [
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
            "counter_agent_name",
            "address",
            "price",
            "total_price",
            "created_at",
        ]

    def get_total_price(self, obj):
        return obj.total_price

    def get_order_type(self, obj):
        return obj.get_product_type_display()

    def get_product_type(self, obj):
        return obj.get_order_type_display()
    
    def get_experience_date(self, obj):
        return obj.experience_date_str

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["status"] = instance.get_status_display()
        products = ["food", "menu", "recipe"]
        for product in products:
            obj = getattr(instance, product, None)
            if obj:
                data[f"{product}_name"] = obj.name
                break
        return data

    def update(self, instance, validated_data):
        status = validated_data.get("status")
        if status is None:
            raise CustomExceptionError(detail="Status most be required", code="400")
        if status == FoodOrder.Status.PENDING:
            raise CustomExceptionError(detail="Status is already pending. Place select other statuses.", code="400")
        if instance.status != FoodOrder.Status.PENDING:
            raise CustomExceptionError(detail="Status is already updated", code="400")
        if instance.status == FoodOrder.Status.ACCEPTED:
            instance.order_ready()
            return instance
        return super().update(instance, validated_data)
