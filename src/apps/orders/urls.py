from django.urls import path

from apps.orders.views.food_order import (
    FoodOrderListAPIView,
    FoodOrderCreateAPIView,
    FoodOrderRetrieveAPIView
)


urlpatterns = [
    path("food_orders/", FoodOrderListAPIView.as_view(), name="food_orders"),
    path("food_order/create/", FoodOrderCreateAPIView.as_view(), name="create_food_order"),
    path("food_order/<str:pk>/", FoodOrderRetrieveAPIView.as_view(), name="food_order"),
]
