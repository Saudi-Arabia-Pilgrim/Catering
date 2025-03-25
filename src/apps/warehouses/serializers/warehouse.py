from apps.base.serializers import CustomModelSerializer
from apps.warehouses.models import Warehouse


class WarehouseSerializer(CustomModelSerializer):
    class Meta:
        model = Warehouse
        exclude = ["created_at", "created_by", "updated_at", "updated_by"]
        read_only_fields = ["status", "count"]