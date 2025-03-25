from apps.base.views import CustomListCreateAPIView, CustomRetrieveAPIView
from apps.warehouses.models import Warehouse
from apps.warehouses.serializers import WarehouseSerializer


class WarehouseRetrieveAPIView(CustomRetrieveAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class WarehouseListCreateAPIView(CustomListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer