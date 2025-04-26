from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.transports.models import Transport


class TransportStatisticListAPIView(CustomGenericAPIView):
    def get(self, *args, **kwargs):
        transports = Transport.objects.all().prefetch_related("order_set")
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
        return Response(data)