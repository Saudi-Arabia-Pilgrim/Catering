from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from apps.base.views import CustomListAPIView
from apps.orders.models import HotelOrder
from apps.orders.serializers.noactive_hotel_guest_food import NoActiveHotelOrderFoodSerializer


class NoActiveHotelOrderListAPIView(CustomListAPIView):
    serializer_class = NoActiveHotelOrderFoodSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["hotel__name"]
    filterset_fields = [
        "check_in", "check_out", "order_status", "hotel__id", "hotel__name"
    ]

    def get_queryset(self):
        return HotelOrder.objects.completed_orders().prefetch_related("guests", "food_order", "room", "hotel")

    def list(self, request, *args, **kwargs):
        queryset= self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
