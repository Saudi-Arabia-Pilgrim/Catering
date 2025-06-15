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
    queryset = HotelOrder.objects.all().select_related("hotel").prefetch_related("hotel__orders")

    def get(self, *args, **kwargs):
        default_diagram_colors = ["#F7B500", "#EB5757", "#2F80ED", "#27AE60"]
        
        orders = self.get_queryset()

        data = []
        total_count = 0
        for order in orders:
            hotel_data = {
                "name": order.hotel.name,
                "value": order.hotel.orders.count(),
            }
            total_count += order.hotel.orders.count()
            data.append(hotel_data)

        data.sort(key=lambda hotel_price: hotel_price["value"], reverse=True)
        first_four = data[:4]
        for_loop = 1
        total_data = []
        for i in first_four:
            if for_loop == 4:
                break
            i["fill"] = default_diagram_colors[for_loop - 1]
            for_loop += 1
            total_data.append(i)
        return Response({"total": total_count, "result": total_data})
