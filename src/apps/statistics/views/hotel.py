from django.db.models import Prefetch
from rest_framework.response import Response

from apps.hotels.models import Hotel
from apps.orders.models import HotelOrder
from apps.statistics.views.abstract import AbstractStatisticsAPIView


class HotelStatisticListAPIView(AbstractStatisticsAPIView):
    queryset = Hotel.objects.all().prefetch_related(
        Prefetch("orders", queryset=HotelOrder.objects.select_related("room"))
    )

    def get(self, *args, **kwargs):
        hotels = self.get_queryset()

        data = []

        for hotel in hotels:
            if hotel.orders.exists():
                hotel_data = {
                    "name": hotel.name,
                    "order_count": hotel.orders.count(),
                    "price": 0,
                }
                for order in hotel.orders.all():
                    hotel_data["price"] += order.profit
                data.append(hotel_data)

        data.sort(key=lambda hotel_price: hotel_price["price"], reverse=True)
        return Response(data)


class HotelDiagramListAPIView(AbstractStatisticsAPIView):
    queryset = Hotel.objects.all().prefetch_related(
        Prefetch("orders", queryset=HotelOrder.objects.select_related("room"))
    )

    def get(self, *args, **kwargs):
        hotels = self.get_queryset()

        data = []
        total_count = 0
        for hotel in hotels:
            if hotel.orders.exists():
                hotel_data = {
                    "name": hotel.name,
                    "order_count": hotel.orders.count(),
                    "precent": 0,
                }
                total_count += hotel.orders.count()
                data.append(hotel_data)

        for hotel in hotels:
            if hotel.orders.exists():
                precent = (hotel.orders.count() / total_count) * 100
                for obj in data:
                    if obj["name"] == hotel.name:
                        data[data.index(obj)]["precent"] = precent
                        break

        data.sort(key=lambda hotel_price: hotel_price["order_count"], reverse=True)
        return Response({"total": total_count, "result": data[:6]})
