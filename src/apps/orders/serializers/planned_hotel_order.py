from apps.base.views import CustomListAPIView
from apps.orders.models import HotelOrder
from apps.orders.serializers import HotelOrderGuestSerializer


class PlannedHotelOrdersAPIView(CustomListAPIView):
    serializer_class = HotelOrderGuestSerializer

    def get_queryset(self):
        return (HotelOrder.objects
                .filter(order_status=HotelOrder.OrderStatus.PLANNED)
                .select_related("hotel", "room")
                .prefetch_related("food_order", "guests"))
