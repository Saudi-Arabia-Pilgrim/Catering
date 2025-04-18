from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from apps.base.views import (
    CustomListCreateAPIView,
    CustomRetrieveUpdateDestroyAPIView,
    CustomGenericAPIView,
)
from apps.foods.models import Food
from apps.foods.serializers import FoodSerializer, FoodCreateUpdateSerializer


class FoodRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all().prefetch_related("recipes", "recipes__product")
    serializer_class = FoodSerializer

    def get_serializer(self, *args, **kwargs):
        if self.request.method in ["PUT", "PATCH"] and self.request.data:
            return FoodCreateUpdateSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)


class FoodListCreateAPIView(CustomListCreateAPIView):
    queryset = Food.objects.all().prefetch_related("recipes", "recipes__product")
    serializer_class = FoodSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["status", "section"]
    search_fields = ["name", "profit", "gross_price"]

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "POST":
            return FoodCreateUpdateSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)


class FoodsOnMenu(CustomGenericAPIView):
    queryset = Food.objects.all().prefetch_related("recipes", "recipes__product")
    serializer_class = FoodSerializer

    def get(self, request, pk):
        queryset = self.get_queryset().filter(menus=pk).prefetch_related("recipes")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)
