from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.orders.models import FoodOrder
from apps.orders.serializers import OnlyFoodOrderSerializer


class FoodOrderListAPIView(CustomGenericAPIView):
    queryset = FoodOrder.objects.all()
    serializer_class = OnlyFoodOrderSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=200)


class FoodOrderCreateAPIView(CustomGenericAPIView):
    queryset = FoodOrder.objects.all()
    serializer_class = OnlyFoodOrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class FoodOrderRetrieveAPIView(CustomGenericAPIView):
    queryset = FoodOrder.objects.all()
    serializer_class = OnlyFoodOrderSerializer

    def get(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)