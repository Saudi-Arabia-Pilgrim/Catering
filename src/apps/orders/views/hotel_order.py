from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.orders.filters import HotelFilterInCreated
from apps.orders.models import HotelOrder
from apps.orders.serializers import HotelOrderGuestSerializer


class HotelOrderListAPIView(CustomGenericAPIView):
    queryset = HotelOrder.objects.all().select_related("hotel", "room",
                                                       ).prefetch_related("guests", "guests__room", "guests__room__room_type")
    serializer_class = HotelOrderGuestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelFilterInCreated


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