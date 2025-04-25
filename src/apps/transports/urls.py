from django.urls import path

from apps.transports.views import (
    TransportCreateAPIView,
    TransportRetrieveUpdateDestroyAPIView,
    TransportListAPIView
)
from apps.transports.views.orders import (
    OrderListAPIView,
    OrderCreateAPIView,
    OrderRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    # Transport URLs
    path("", TransportListAPIView.as_view(), name="transport_list"),
    path("create/", TransportCreateAPIView.as_view(), name="transport_create"),
    path("<uuid:pk>/", TransportRetrieveUpdateDestroyAPIView.as_view(), name="transport_detail"),

    # Order URLs
    path("orders/", OrderListAPIView.as_view(), name="order_list"),
    path("orders/create/", OrderCreateAPIView.as_view(), name="order_create"),
    path("orders/<uuid:pk>/", OrderRetrieveUpdateDestroyAPIView.as_view(), name="order_detail"),
]