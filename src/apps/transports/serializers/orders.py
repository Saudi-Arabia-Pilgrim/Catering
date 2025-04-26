from apps.base.serializers import CustomModelSerializer
from apps.transports.models import Order


class OrderSerializer(CustomModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "order_number",
            "transport",
            "perform_date",
            "from_location",
            "to_location",
            "status",
            "passenger_count",
            "service_fee",
            "gross_fee"
        )
        read_only_fields = (
            "id",
            "order_number",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        )
