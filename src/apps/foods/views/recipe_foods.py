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
from apps.warehouses.utils import validate_uuid


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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        count = serializer.validated_data.get("count")
        product = serializer.validated_data.get("product")

        instance, created = RecipeFood.objects.get_or_create(
            count=count,
            product=product,
            defaults=serializer.validated_data
        )

        output_serializer = self.get_serializer(instance)
        return Response(output_serializer.data, status=201 if created else 200)


class RecipeFoodsOnFood(CustomGenericAPIView):
    queryset = RecipeFood.objects.all().select_related("product")
    serializer_class = RecipeFoodSerializer

    def get(self, request, pk):
        validate_uuid(pk)
        queryset = self.get_queryset().filter(foods=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)
