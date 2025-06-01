from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from apps.base.views import CustomRetrieveAPIView, CustomListCreateAPIView
from apps.base.views.generics import CustomGenericAPIView
from apps.orders.models import FoodOrder
from apps.orders.serializers import OnlyFoodOrderSerializer, FoodOrderRetrieveSerializer
from apps.warehouses.utils import validate_uuid


class FoodOrderListCreateAPIView(CustomListCreateAPIView):
    queryset = FoodOrder.objects.all().order_by("-created_at")
    serializer_class = OnlyFoodOrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["product_type", "order_type", "counter_agent", "order_type", "order_time"]
    search_fields = ["food_order_id", "counter_agent__name", "created_at"]


class FoodOrderRetrieveAPIView(CustomRetrieveAPIView):
    queryset = (
        FoodOrder.objects.all()
        .order_by("-created_at")
        .select_related(
            "food",
            "menu",
            "recipe",
            "counter_agent",
            "recipe__menu_breakfast",
            "recipe__menu_lunch",
            "recipe__menu_dinner",
        )
        .prefetch_related("menu__foods")
    )
    serializer_class = FoodOrderRetrieveSerializer


class ReadyFodOrderAPIView(CustomGenericAPIView):
    queryset = FoodOrder.objects.all().order_by("-created_at")
    serializer_class = FoodOrderRetrieveSerializer

    def get(self, request, pk):
        validate_uuid(pk)
        instance = get_object_or_404(FoodOrder, pk=pk)
        instance.order_ready()
        return Response("The order is ready", status=200)
