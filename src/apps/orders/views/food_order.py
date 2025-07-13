from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from apps.base.views import CustomRetrieveUpdateAPIView, CustomListCreateAPIView
from apps.orders.models import FoodOrder
from apps.orders.serializers import OnlyFoodOrderSerializer, FoodOrderRetrieveSerializer


class FoodOrderListCreateAPIView(CustomListCreateAPIView):
    queryset = FoodOrder.objects.all().order_by("-created_at")
    serializer_class = OnlyFoodOrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["product_type", "order_type", "counter_agent", "order_type", "order_time", "status"]
    search_fields = ["food_order_id", "counter_agent__name", "created_at"]


class FoodOrderRetrieveUpdateAPIView(CustomRetrieveUpdateAPIView):
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
