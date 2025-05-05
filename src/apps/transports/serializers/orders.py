from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.transports.models import Order


class OrderSerializer(CustomModelSerializer):
    transport_model_name = serializers.CharField(source="transport.name", read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "transport",
            "order_number",
            "perform_date",
            "from_location",
            "to_location",
            "status",
            "passenger_count",
            "service_fee",
            "gross_fee",
            "transport_model_name",
        )
        read_only_fields = (
            "id",
            "order_number",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        )
