from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.products.models import Product


class ProductSerializer(CustomModelSerializer):
    measure_abbreviation = serializers.CharField(source="measure.abbreviation", read_only=True)
    section_name = serializers.CharField(source="section.name", read_only=True)
    measure_warehouse_abbreviation = serializers.CharField(source="measure.abbreviation", read_only=True)

    class Meta:
        model = Product
        exclude = ["slug", "created_at", "created_by", "updated_at", "updated_by"]
        write_only_fields = ["measure", "difference_measures", "section"]
        read_only_fields = ["status"]