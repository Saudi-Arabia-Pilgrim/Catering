from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from apps.base.views import CustomCreateAPIView
from apps.orders.filters import HotelOrderFilter
from apps.orders.models.hotel_order import HotelOrder
from apps.orders.serializers import ActiveHotelOrderFoodSerializer, HotelOrderCreateSerializer


class ActiveHotelOrderListAPIView(generics.ListAPIView):
    serializer_class = ActiveHotelOrderFoodSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = HotelOrderFilter
    search_fields = ["hotel__name"]

    def get_queryset(self):
        return HotelOrder.objects.active_orders().prefetch_related("guests", "food_order", "room", "hotel")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class HotelFoodOrderCreateAPIView(CustomCreateAPIView):
    queryset = HotelOrder.objects.all()
    serializer_class = HotelOrderCreateSerializer