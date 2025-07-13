from django.urls import path

from apps.orders.serializers.planned_hotel_order import PlannedHotelOrdersAPIView
from apps.orders.views import (HotelOrderCreateAPIView,
                               HotelOrderListAPIView,
                               HotelOrderRetrieveAPIView,
                               HotelOrderDeleteAPIView)
from apps.orders.views.active_orders import ActiveHotelOrderListAPIView
from apps.orders.views.food_order import (FoodOrderListCreateAPIView,
                                          FoodOrderRetrieveAPIView,
                                          ReadyFodOrderAPIView)
from apps.orders.views.noactive_orders import NoActiveHotelOrderListAPIView

urlpatterns = [
    # ===================  Food Orders ===================
    path("food_orders/", FoodOrderListCreateAPIView.as_view(), name="food_orders_create_list"),
    path("food_orders/<str:pk>/", FoodOrderRetrieveAPIView.as_view(), name="food_order_retrieve"),
    path("food_orders/ready/<str:pk>/", ReadyFodOrderAPIView.as_view(), name="food_order_ready"),

    # ===================  Hotel Orders ===================
    path("hotel_orders/", HotelOrderListAPIView.as_view(), name="hotel_orders"),
    path("hotel_order/create/", HotelOrderCreateAPIView.as_view(), name="create_hotel_orders"),
    path("hotel_order/<str:pk>/", HotelOrderRetrieveAPIView.as_view(), name="hotel_order"),
    path("hotel_order/delete/<str:pk>/", HotelOrderDeleteAPIView.as_view(), name="hotel_order_delete"),

    # ========================== ACTIVE Orders =======================
    path('hotel_orders/active/', ActiveHotelOrderListAPIView.as_view(), name='active-orders-list'),

    # ========================== NO ACTIVE ORDERS ==========================
    path("hotel_orders/no-active/", NoActiveHotelOrderListAPIView.as_view(), name="no-active-orders-list"),

    # ========================== PLANNED ORDERS ==========================
    path("hotel_orders/planned/", PlannedHotelOrdersAPIView.as_view(), name="planned-orders-list")
]
