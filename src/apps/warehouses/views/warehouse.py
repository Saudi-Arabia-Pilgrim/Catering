from decimal import Decimal
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from apps.base.views import CustomListCreateAPIView, CustomGenericAPIView
from apps.warehouses.models import Warehouse, Experience
from apps.warehouses.serializers import WarehouseSerializer, WarehouseExpensesSerializer
from apps.warehouses.utils import validate_uuid


class WarehouseExpensesRetrieveAPIView(CustomGenericAPIView):
    queryset = Warehouse.objects.all().select_related("product", "product__measure_warehouse", "product__measure")
    serializer_class = WarehouseSerializer

    def get(self, request, pk):
        validate_uuid(pk)
        warehouse = get_object_or_404(Warehouse, pk=pk)
        serializer = self.get_serializer(warehouse)
        return Response(serializer.data, status=200)

    def post(self, request, pk):
        validate_uuid(pk)
        warehouse = get_object_or_404(Warehouse, pk=pk)
        serializer = self.get_serializer(
            data=request.data, context={"warehouse": warehouse}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        validated_data = serializer.validated_data
        data = f"{validated_data["amount"]}{validated_data["measure_abbreviation"]} {validated_data["product_name"]} were successfully removed from the warehouse"
        price = Decimal(warehouse.get_net_price()) * Decimal(warehouse.product.difference_measures) * Decimal(validated_data["amount"])
        Experience.objects.create(
            warehouse=warehouse, count=validated_data["amount"], price=price
        )
        return Response(data, status=200)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return WarehouseExpensesSerializer
        return super().get_serializer_class()


class WarehouseListCreateAPIView(CustomListCreateAPIView):
    queryset = Warehouse.objects.all().select_related(
        "product", "product__measure_warehouse", "product__measure"
    )
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {
        "status": ["exact"],
        "created_at": ["gte", "lte", "range"],
        "product__section": ["exact"],
        "product__measure_warehouse": ["exact"],
    }
    search_fields = ["product__name"]
