from rest_framework import serializers

from apps.base.exceptions.exception_error import CustomExceptionError
from apps.base.serializers import CustomModelSerializer, CustomSerializer
from apps.warehouses.models import Warehouse


class WarehouseSerializer(CustomModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    amount = serializers.FloatField(source="count", read_only=True)
    arrived_amount = serializers.FloatField(source="arrived_count")

    measure = serializers.CharField(
        source="product.measure_warehouse.abbreviation", read_only=True
    )
    image = serializers.SerializerMethodField(read_only=True)
    section = serializers.CharField(source="product.section.name", read_only=True)

    class Meta:
        model = Warehouse
        exclude = ["created_by", "updated_at", "updated_by", "count", "arrived_count"]
        read_only_fields = ["status"]

    def get_image(self, obj):
        request = self.context.get("request")
        image = obj.product.image
        if image and request:
            return request.build_absolute_uri(image.url)
        return None


class WarehouseExpensesSerializer(CustomSerializer):
    amount = serializers.IntegerField(write_only=True)

    def validate(self, validated_data):
        amount = validated_data["amount"]
        warehouse = self.context["warehouse"]
        product = warehouse.product
        if amount > warehouse.count:
            raise CustomExceptionError(
                code=400,
                detail="The amount exceeds the available stock in the warehouse.",
            )
        validated_data["product_name"] = product.name
        validated_data["measure_abbreviation"] = product.measure_warehouse.abbreviation
        return validated_data

    def save(self):
        warehouse = self.context["warehouse"]
        warehouse.count = warehouse.count - self.validated_data["amount"]
        warehouse.save()
