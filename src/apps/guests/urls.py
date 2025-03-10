from django.urls import path

from apps.guests.views import AddGuestAPIView
from apps.guests.views.guests import HotelGuestListAPIView


urlpatterns = [
    path("hotels/<str:hotel_id>/", HotelGuestListAPIView.as_view(), name="hotel_guests"),
    path("hotels/<str:hotel_id>/add/", AddGuestAPIView.as_view(), name="add_guest"),
]