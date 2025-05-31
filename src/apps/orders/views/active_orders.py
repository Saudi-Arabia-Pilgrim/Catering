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
    """
       API View to retrieve a list of currently active hotel orders.

       This endpoint returns data for all hotel orders that are currently active. It allows
       searching by hotel name and returns rich nested data, including guests, their rooms,
       room types, and related food orders.

         **Example Request**:
            GET /api/v1/hotels/14690dfa-f331-405a-aeea-61cfd429ee64/

         **Example Request with Filtering by Room Type**:
            GET /api/v1/hotels/14690dfa-f331-405a-aeea-61cfd429ee64/?room_type=134a7b13-924f-4e16-825c-86eb07a1a2ee

       🏨 Related Prefetched Data:
       - Guests and their linked rooms and room types
       - Food orders
       - Hotel-level guests and their rooms
       Example Queries:
            - `/api/v1/orders/active/?search=Hilton`
            - `/api/v1/orders/active/?created_at_after=2025-01-01&created_at_before=2025-01-31`
            - `/api/v1/orders/active/?check_in__gte=2025-02-01&check_out__lte=2025-02-10`
       """
    serializer_class = ActiveHotelOrderFoodSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["hotel__name"]

    def get_queryset(self):
        return HotelOrder.objects.active_orders().select_related("hotel", "room").prefetch_related("guests",
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
