from django.urls import path

from apps.orders.views.add_guest_to_hotel_order import AddGuestToHotelOrderAPIView
from apps.orders.views import (HotelOrderCreateAPIView,
                               HotelOrderListAPIView,
                               HotelOrderRetrieveAPIView,
                               HotelOrderUpdateAPIView,
                               HotelOrderDeleteAPIView)

from apps.orders.views.food_order import (FoodOrderListAPIView,
                                          FoodOrderCreateAPIView,
                                          FoodOrderRetrieveAPIView)


urlpatterns = [
    # ===================  Food Orders ===================
    path("food_orders/", FoodOrderListAPIView.as_view(), name="food_orders"),
    path("food_order/create/", FoodOrderCreateAPIView.as_view(), name="create_food_order"),
    path("food_order/<str:pk>/", FoodOrderRetrieveAPIView.as_view(), name="food_order"),

    # ===================  Hotel Orders ===================
    path("hotel_orders/", HotelOrderListAPIView.as_view(), name="hotel_orders"),
    path("hotel_order/create/", HotelOrderCreateAPIView.as_view(), name="create_hotel_orders"),
    path("hotel_order/<str:pk>/", HotelOrderRetrieveAPIView.as_view(), name="hotel_order"),
    path("hotel_order/update/<str:pk>/", HotelOrderUpdateAPIView.as_view(), name="hotel_order_update"),
    path("hotel_order/delete/<str:pk>/", HotelOrderDeleteAPIView.as_view(), name="hotel_order_delete"),

    # ===================  Add Guest for HotelOrder ==========================
    path("hotel_order/add-guests/<str:pk>/", AddGuestToHotelOrderAPIView.as_view(), name="hotel-order-add-guests"),
]
