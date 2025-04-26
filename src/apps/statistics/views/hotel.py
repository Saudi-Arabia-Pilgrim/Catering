from django.db.models import Prefetch
from rest_framework.response import Response

from apps.hotels.models import Hotel
from apps.orders.models import HotelOrder
from apps.base.views import CustomGenericAPIView


class HotelStatisticListAPIView(CustomGenericAPIView):
    def get(self, *args, **kwargs):
        hotels = Hotel.objects.all().prefetch_related(
            Prefetch(
                "orders",
                queryset=HotelOrder.objects.select_related("room")
            )
        )

        data = []

        for hotel in hotels:
            if hotel.orders.exists():
                hotel_data = {
                    "name": hotel.name,
                    "order_count": hotel.orders.count(),
                    "price": 0
                }
                for order in hotel.orders.all():
                    hotel_data["price"] += order.profit
                data.append(hotel_data)

        data.sort(key=lambda hotel_price: hotel_price["price"], reverse=True)
        return Response(data)
