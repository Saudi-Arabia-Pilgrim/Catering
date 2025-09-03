from django.urls import path

from apps.guests.views.guests import GuestListAPIView, GuestOfHotelListAPIView

urlpatterns = [
    path("", GuestListAPIView.as_view(), name="guest-lists"),
    path("of-hotel/<str:pk>/", GuestOfHotelListAPIView.as_view(), name="guest-of-hotel-lists"),
]