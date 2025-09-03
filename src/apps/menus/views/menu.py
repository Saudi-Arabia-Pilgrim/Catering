from django.db.models import Q

from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from apps.base.views import (
    CustomListCreateAPIView,
    CustomRetrieveUpdateDestroyAPIView,
    CustomGenericAPIView,
)
from apps.menus.models import Menu
from apps.menus.serializers import MenuSerializer, MenuCreateUpdateSerializer
from apps.warehouses.utils import validate_uuid


class MenuRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all().prefetch_related("foods")
    serializer_class = MenuSerializer

    def get_serializer(self, *args, **kwargs):
        if self.request.method in ["PUT", "PATCH"] and self.request.data:
            return MenuCreateUpdateSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)


class MenuListCreateAPIView(CustomListCreateAPIView):
    queryset = Menu.objects.all().prefetch_related("foods")
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["status", "menu_type"]
    search_fields = ["name", "gross_price", "profit"]

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "POST":
            return MenuCreateUpdateSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)


class MenusOnRecipe(CustomGenericAPIView):
    queryset = Menu.objects.all().prefetch_related("foods")
    serializer_class = MenuSerializer

    def get(self, request, pk):
        validate_uuid(pk)
        queryset = (
            self.get_queryset()
            .filter(
                Q(breakfast_recipes__id=pk)
                | Q(lunch_recipes__id=pk)
                | Q(dinner_recipes__id=pk)
            )
            .prefetch_related("foods")
            .distinct()
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)
