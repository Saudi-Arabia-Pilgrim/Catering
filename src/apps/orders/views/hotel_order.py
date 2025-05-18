from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
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
    queryset = HotelOrder.objects.all().select_related("hotel", "room",
                                                       ).prefetch_related("guests", "guests__room", "guests__room__room_type")
    serializer_class = HotelOrderGuestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {"created_at": ["range"], "check_in": ["range"], "check_out": ["range"]}


    def get(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=200)


class HotelOrderCreateAPIView(CustomGenericAPIView):
    queryset = HotelOrder.objects.all().prefetch_related("guests", "guests__room", "guests__room__room_type", "room__room_type")
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