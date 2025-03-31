from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from apps.base.views import CustomListCreateAPIView, CustomGenericAPIView
from apps.warehouses.models import Warehouse
from apps.warehouses.serializers import WarehouseSerializer, WarehouseExpensesSerializer


class WarehouseExpensesRetrieveAPIView(CustomGenericAPIView):
    queryset = Warehouse.objects.all().select_related("product")
    serializer_class = WarehouseSerializer

    def get(self, request, pk):
        warehouse = get_object_or_404(Warehouse, pk=pk)
        serializer = self.get_serializer(warehouse)
        return Response(serializer.data, status=200)

    def post(self, request, pk):
        warehouse = get_object_or_404(Warehouse, pk=pk)
        serializer = self.get_serializer(data=request.data,
                                         context={"warehouse": warehouse})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        validated_data = serializer.validated_data
        data = f"{validated_data["count"]}{validated_data["measure_abbreviation"]} {validated_data["product_name"]} were successfully removed from the warehouse"
        return Response(data, status=200)
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return WarehouseExpensesSerializer
        return super().get_serializer_class()


class WarehouseListCreateAPIView(CustomListCreateAPIView):
    queryset = Warehouse.objects.all().select_related("product")
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {
        "status": ["exact"],
        "created_at": ["gte", "lte", "range"]
    }
    search_fields = ["product__name", "name", "warehouse_id"]