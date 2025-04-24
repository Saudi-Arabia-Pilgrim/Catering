from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from apps.base.views import (
    CustomListCreateAPIView,
    CustomRetrieveUpdateDestroyAPIView,
    CustomGenericAPIView,
)
from apps.foods.models import RecipeFood
from apps.foods.serializers import RecipeFoodSerializer, RecipeUpdateFoodSerializer


class RecipeFoodRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    queryset = RecipeFood.objects.all().select_related("product")
    serializer_class = RecipeFoodSerializer

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return RecipeUpdateFoodSerializer
        return super().get_serializer_class()


class RecipeFoodListCreateAPIView(CustomListCreateAPIView):
    queryset = RecipeFood.objects.all().select_related("product")
    serializer_class = RecipeFoodSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["status"]
    search_fields = ["product__name", "count", "price"]


class RecipeFoodsOnFood(CustomGenericAPIView):
    queryset = RecipeFood.objects.all().select_related("product")
    serializer_class = RecipeFoodSerializer

    def get(self, request, pk):
        queryset = self.get_queryset().filter(foods=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)
