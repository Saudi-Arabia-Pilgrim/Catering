from rest_framework.response import Response

from apps.base.pagination import CustomPageNumberPagination
from apps.statistics.views.abstract import AbstractStatisticsAPIView
from apps.transports.models import Transport


class TransportStatisticListAPIView(AbstractStatisticsAPIView):
    queryset = Transport.objects.all().prefetch_related("order_set")

    def get(self, request, *args, **kwargs):
        transports = self.get_queryset()
        data = []

        for transport in transports:
            if transport.order_set.exists():
                transport_data = {
                    "name": transport.name_of_driver,
                    "car": transport.name,
                    "order_count": transport.order_set.count(),
                    "price": 0
                }
                for order in transport.order_set.all():
                    transport_data["price"] += order.profit
                data.append(transport_data)
            data.sort(key=lambda y: y["price"], reverse=True)
        paginator = CustomPageNumberPagination()
        paginated_data = paginator.paginate_queryset(data, request)
        return paginator.get_paginated_response(paginated_data)