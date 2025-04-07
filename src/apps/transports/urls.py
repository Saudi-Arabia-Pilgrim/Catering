from django.urls import path
from apps.transports.views import (
    TransportCreateAPIView,
    TransportRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path("", TransportCreateAPIView.as_view(), name="transport_create"),
    path("<int:pk>/", TransportRetrieveUpdateDestroyAPIView.as_view(), name="transport_detail"),
]