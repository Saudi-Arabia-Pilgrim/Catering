from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from apps.guests.models import Guest
from apps.orders.models import HotelOrder
from apps.rooms.models import Room, RoomType
from apps.base.views import CustomListAPIView
from apps.orders.serializers.noactive_hotel_guest_food import NoActiveHotelOrderFoodSerializer


class NoActiveHotelOrderListAPIView(CustomListAPIView):
    serializer_class = NoActiveHotelOrderFoodSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["hotel__name"]
    filterset_fields = {"created_at": ["range"], "check_in": ["gte"], "check_out": ["lte"]}
    
    def get_queryset(self):
        return HotelOrder.objects.completed_orders().select_related("hotel").prefetch_related("guests",
                                                                                           "guests__room",
                                                                                           "guests__room__room_type",
                                                                                           "food_order",
                                                                                           Prefetch("hotel__guests", queryset=Guest.objects.all()),
                                                                                           Prefetch("hotel__guests__room", queryset=Room.objects.all()),
                                                                                           Prefetch("hotel__guests__room__room_type", queryset=RoomType.objects.all()))

    def list(self, request, *args, **kwargs):
        queryset= self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
