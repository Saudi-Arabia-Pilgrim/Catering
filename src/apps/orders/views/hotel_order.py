from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.orders.models import HotelOrder
from apps.orders.serializers import HotelOrderSerializer


class HotelOrderListAPIView(CustomGenericAPIView):
    queryset = HotelOrder.objects.all()
    serializer_class = HotelOrderSerializer

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=200)


class HotelOrderCreateAPIView(CustomGenericAPIView):
    queryset = HotelOrder.objects.all()
    serializer_class = HotelOrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(self.get_serializer(order).data, status=201)


class HotelOrderRetrieveAPIView(CustomGenericAPIView):
    queryset = HotelOrder.objects.all()
    serializer_class = HotelOrderSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)


class HotelOrderUpdateAPIView(CustomGenericAPIView):
    queryset = HotelOrder.objects.all()
    serializer_class = HotelOrderSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


class HotelOrderDeleteAPIView(CustomGenericAPIView):
    queryset = HotelOrder.objects.all()
    serializer_class = HotelOrderSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(instance)