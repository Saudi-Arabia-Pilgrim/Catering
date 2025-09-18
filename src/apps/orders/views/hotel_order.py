from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.orders.filters import HotelFilterForGuests
from apps.orders.models import HotelOrder
from apps.orders.serializers import HotelOrderGuestSerializer


class HotelOrderListAPIView(CustomGenericAPIView):
    """
    🏨 Hotel Order List API View 🛎️

    Fetches a list of hotel orders with their rooms and guests.
    It's like peeking into who booked what, when, and for how long, without disturbing the guests (no room service included).

    Usage:
    - GET request to retrieve filtered hotel orders.
    - Pass date ranges to filter fields like `created_at`, `check_in`, and `check_out` in query params.
      Example: _?created_at_after=2024-01-01&created_at_before=2024-01-31

    Warning:
    - This API will NOT bring you breakfast in bed. For that, contact room service. 😎

    Returns:
    - Paginated list of hotel orders with detailed guest and room info.
    """
    queryset = HotelOrder.objects.select_related(
        "hotel", "room", "room__room_type"
    ).prefetch_related(
        "guests", "guests__room", "guests__room__room_type",
        "food_order", "food_order__counter_agent"
    )

    serializer_class = HotelOrderGuestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelFilterForGuests

    @extend_schema(
        summary="List hotel orders with date and hotel filters",
        parameters=[
            OpenApiParameter("room_type", OpenApiTypes.INT, OpenApiParameter.QUERY,
                             description="Filter orders by Room Type"),
            OpenApiParameter("created_at_after", OpenApiTypes.DATE, OpenApiParameter.QUERY,
                             description="Start date for created_at"),
            OpenApiParameter("created_at_before", OpenApiTypes.DATE, OpenApiParameter.QUERY,
                             description="End date for created_at"),
            OpenApiParameter("check_in_after", OpenApiTypes.DATE, OpenApiParameter.QUERY,
                             description="Start date for check-in"),
            OpenApiParameter("check_in_before", OpenApiTypes.DATE, OpenApiParameter.QUERY,
                             description="End date for check-in"),
            OpenApiParameter("check_out_after", OpenApiTypes.DATE, OpenApiParameter.QUERY,
                             description="Start date for check-out"),
            OpenApiParameter("check_out_before", OpenApiTypes.DATE, OpenApiParameter.QUERY,
                             description="End date for check-out"),
            OpenApiParameter("hotel", OpenApiTypes.INT, OpenApiParameter.QUERY,
                             description="Hotel ID to filter orders by"),
            OpenApiParameter("page", OpenApiTypes.INT, OpenApiParameter.QUERY, description="Pagination page number"),
        ]
    )
    def get(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=200)


class HotelOrderCreateAPIView(CustomGenericAPIView):
    queryset = HotelOrder.objects.select_related("room", "room__room_type", "guest_group").prefetch_related(
        "guests", "guests__room", "guests__room__room_type", "food_order", "food_order__counter_agent"
    )
    serializer_class = HotelOrderGuestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(self.get_serializer(order).data, status=201)


class HotelOrderRetrieveAPIView(CustomGenericAPIView):
    queryset = HotelOrder.objects.all()
    serializer_class = HotelOrderGuestSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)


class HotelOrderDeleteAPIView(CustomGenericAPIView):
    queryset = HotelOrder.objects.all()
    serializer_class = HotelOrderGuestSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)