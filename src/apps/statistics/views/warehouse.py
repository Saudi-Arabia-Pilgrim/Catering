import calendar

from rest_framework.response import Response

from apps.base.pagination import CustomPageNumberPagination
from apps.base.views import CustomGenericAPIView
from apps.orders.models import FoodOrder
from apps.statistics.utils import iterate_months, validate_from_and_date_to_date, round_up_to_nice_number
from apps.statistics.views.abstract import AbstractStatisticsAPIView
from apps.warehouses.models import Warehouse, ProductsUsed, Experience


class CheckoutListAPIView(AbstractStatisticsAPIView):
    queryset = Experience.objects.all().select_related(
        "warehouse",
        "warehouse__product",
        "warehouse__product__section",
        "warehouse__product__measure",
    )

    def get(self, request, *args, **kwargs):
        experiences = self.get_queryset()
        data = {}

        for experience in experiences:
            product = experience.warehouse.product
            measure_warehouse = product.measure_warehouse
            name = product.name

            count_value = experience.count

            if name not in data:
                data[name] = {
                    "measure": measure_warehouse.abbreviation,
                    "count": count_value,
                    "section": product.section.name,
                    "price": experience.price,
                    "image": (
                        request.build_absolute_uri(product.image.url)
                        if product.image
                        else None
                    ),
                }
            else:
                data[name]["count"] += count_value
                data[name]["price"] += experience.price

        data_list = [
            {"name": name, **details} for name, details in data.items()
        ]

        paginator = CustomPageNumberPagination()
        paginated_data = paginator.paginate_queryset(data_list, request)
        return paginator.get_paginated_response(paginated_data)


class CheckInListAPIView(AbstractStatisticsAPIView):
    queryset = Warehouse.objects.all().select_related(
        "product", "product__measure", "product__section"
    )

    def get(self, request, *args, **kwargs):
        warehouses = self.get_queryset()
        data = {}

        for warehouse in warehouses:
            name = warehouse.product.name
            if name not in data:
                data[name] = {
                    "measure": warehouse.product.measure_warehouse.abbreviation,
                    "count": warehouse.arrived_count,
                    "section": warehouse.product.section.name,
                    "price": warehouse.gross_price,
                    "image": (
                        request.build_absolute_uri(warehouse.product.image.url)
                        if warehouse.product.image
                        else None
                    ),
                }
            else:
                data[name]["count"] += warehouse.arrived_count
                data[name]["price"] += warehouse.gross_price

        data_list = [
            {"name": name, **details} for name, details in data.items()
        ]

        paginator = CustomPageNumberPagination()
        paginated_data = paginator.paginate_queryset(data_list, request)
        return paginator.get_paginated_response(paginated_data)


class MostUsedProductsListAPIView(AbstractStatisticsAPIView):
    queryset = ProductsUsed.objects.all().select_related(
        "warehouse", "warehouse__product", "warehouse__product__measure_warehouse", "warehouse__product__section"
    )

    def get(self, request, *args, **kwargs):
        used_products = self.get_queryset()
        data = {}

        for used_product in used_products:
            product = used_product.warehouse.product
            name = product.name

            count = float(used_product.count)
            price = float(used_product.price)

            if name not in data:
                data[name] = {
                    "measure": product.measure_warehouse.abbreviation,
                    "count": count,
                    "section": product.section.name,
                    "price": price,
                    "image": (
                        request.build_absolute_uri(product.image.url)
                        if product.image else None
                    ),
                }
            else:
                data[name]["count"] += count
                data[name]["price"] += price

        data_list = [
            {"name": name, **details} for name, details in data.items()
        ]

        paginator = CustomPageNumberPagination()
        paginated_data = paginator.paginate_queryset(data_list, request)
        return paginator.get_paginated_response(paginated_data)



class CheckInCheckoutDiagramAPIView(CustomGenericAPIView):
    def get(self, request, *args, **kwargs):

        from_date, to_date = validate_from_and_date_to_date(request)

        data = []

        warehouses = list(
            Warehouse.objects.filter(created_at__lte=to_date, created_at__gte=from_date)
        )
        orders = list(
            FoodOrder.objects.filter(
                created_at__lte=to_date, created_at__gte=from_date, status=FoodOrder.Status.ACCEPTED
            )
        )

        for month_date in iterate_months(from_date, to_date):

            month_warehouses = []
            month_orders = []
            month_name = calendar.month_name[month_date.month]

            for warehouse in warehouses:
                if warehouse.created_at.month == month_date.month:
                    month_warehouses.append(warehouse)

            for order in orders:
                if order.created_at.month == month_date.month:
                    month_orders.append(order)

            diagram = {
                "name": month_name,
                "checkout": 0,
                "check_in": 0,
            }

            for warehouse in month_warehouses:
                diagram["check_in"] = int(diagram["check_in"] + warehouse.gross_price)

            for order in month_orders:
                diagram["checkout"] = int(diagram["checkout"] + order.profit)
            data.append(diagram)

        max_raw = max(
            max(d["check_in"], d["checkout"]) for d in data
        )

        max_y = round_up_to_nice_number(max_raw)

        return Response({"data": data, "max_y": max_y})
