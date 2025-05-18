from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from apps.base.views import CustomCreateAPIView, CustomListAPIView
from apps.guests.models import Guest
from apps.orders.models.hotel_order import HotelOrder
from apps.orders.serializers import ActiveHotelOrderFoodSerializer, HotelOrderCreateSerializer
from apps.rooms.models import Room, RoomType


class ActiveHotelOrderListAPIView(CustomListAPIView):
    serializer_class = ActiveHotelOrderFoodSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["hotel__name"]

    def get_queryset(self):
        return HotelOrder.objects.active_orders().select_related("hotel").prefetch_related("guests",
                                                                                           "guests__room",
                                                                                           "guests__room__room_type",
                                                                                           "food_order",
                                                                                           Prefetch("hotel__guests", queryset=Guest.objects.all()),
                                                                                           Prefetch("hotel__guests__room", queryset=Room.objects.all()),
                                                                                           Prefetch("hotel__guests__room__room_type", queryset=RoomType.objects.all()))

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