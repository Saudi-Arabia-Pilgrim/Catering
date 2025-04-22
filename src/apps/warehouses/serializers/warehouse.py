from rest_framework import serializers

from apps.base.exceptions.exception_error import CustomExceptionError
from apps.base.serializers import CustomModelSerializer, CustomSerializer
from apps.warehouses.models import Warehouse


class WarehouseSerializer(CustomModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = Warehouse
        exclude = ["created_by", "updated_at", "updated_by"]
        read_only_fields = ["status",
                            "count",
                            "warehouse_id",
                            # "name",
                            ]
        # required_fields = ["name_uz", "name_ru", "name_ar", "name_en"]


class WarehouseExpensesSerializer(CustomSerializer):
    count = serializers.IntegerField(write_only=True)

    def validate(self, validated_data):
        count = validated_data["count"]
        warehouse = self.context["warehouse"]
        product = warehouse.product
        difference_measures = product.difference_measures
        if (
            count
            > (warehouse.count * difference_measures if difference_measures else 1)
            or count == 0
        ):
            raise CustomExceptionError(
                code=400,
                detail="The count exceeds the available stock in the warehouse.",
            )
        validated_data["product_name"] = product.name
        validated_data["measure_abbreviation"] = product.measure.abbreviation
        return validated_data

    def save(self):
        warehouse = self.context["warehouse"]
        difference_measures = warehouse.product.difference_measures
        warehouse.count = warehouse.count - (
            self.validated_data["count"] / difference_measures
            if difference_measures
            else 1
        )
        warehouse.save()
