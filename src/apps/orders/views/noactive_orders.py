from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from apps.guests.models import Guest
from apps.orders.filters import HotelFilterForGuests
from apps.orders.models import HotelOrder
from apps.rooms.models import Room, RoomType
from apps.base.views import CustomListAPIView
from apps.orders.serializers.noactive_hotel_guest_food import NoActiveHotelOrderSerializer


class NoActiveHotelOrderListAPIView(CustomListAPIView):
    """
        API View to retrieve a list of completed hotel orders that are no longer active.

        This endpoint returns a list of completed hotel orders (i.e., orders that are not currently active).
        It supports advanced filtering, searching, and pagination for efficient data access.

         **Example Request**:
        GET /api/v1/hotels/14690dfa-f331-405a-aeea-61cfd429ee64/

          **Example Request with Filtering by Room Type**:
        GET /api/v1/hotels/14690dfa-f331-405a-aeea-61cfd429ee64/?room_type=134a7b13-924f-4e16-825c-86eb07a1a2ee

        🔍 Example Queries:
            - `/api/v1/orders/no-active/?search=Hilton`
            - `/api/v1/orders/no-active/?created_at_after=2025-01-01&created_at_before=2025-01-31`
            - `/api/v1/orders/no-active/?check_in__gte=2025-02-01&check_out__lte=2025-02-10`

        """
    serializer_class = NoActiveHotelOrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["hotel__name"]
    filterset_fields = {"created_at": ["range"], "check_in": ["gte"], "check_out": ["lte"]}
    filterset_class = HotelFilterForGuests

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
