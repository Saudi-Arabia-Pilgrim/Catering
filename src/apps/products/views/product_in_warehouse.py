from decimal import Decimal

from django.db.models import Sum

from rest_framework.response import Response

from apps.base.exceptions.exception_error import CustomExceptionError
from apps.base.views.generics import CustomGenericAPIView
from apps.warehouses.models import Warehouse
from apps.warehouses.utils import validate_uuid


class ProductInWarehouse(CustomGenericAPIView):
    def get(self, request, pk, *args, **kwargs):
        validate_uuid(pk)

        warehouses = Warehouse.objects.filter(
            product_id=pk, status=True, count__gt=0
        ).order_by("created_at").select_related("product")

        if not warehouses.exists():
            raise CustomExceptionError(
                code=400,
                detail="The warehouse with the specified product ID was not found or the products in it are out of stock.",
            )

        first_warehouse = warehouses.first()
        data = {
            "count": str(warehouses.aggregate(total=Sum("count"))["total"] or Decimal('0')),
            "price": str(first_warehouse.get_net_price()),
            "measure": first_warehouse.product.measure_warehouse.abbreviation
        }

        return Response(data)
