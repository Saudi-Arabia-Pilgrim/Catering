from django.urls import path

from apps.guests.views.guests_group import GuestGroupListAPIView, GuestGroupCreateAPIView, \
    GuestGroupRetrieveUpdateAPIView, GuestGroupDeleteAPIView
from apps.guests.views.guests import GuestListAPIView, GuestOfHotelListAPIView


urlpatterns = [
    path("", GuestListAPIView.as_view(), name="guest-lists"),
    path("of-hotel/<str:pk>/", GuestOfHotelListAPIView.as_view(), name="guest-of-hotel-lists"),

    # ============= Guest Group Endpoints =====================
    path("groups/", GuestGroupListAPIView.as_view(), name="guests-group-list"),
    path("groups/create", GuestGroupCreateAPIView.as_view(), name="guests-group-create"),
    path("groups/update/<str:pk>/", GuestGroupRetrieveUpdateAPIView.as_view(), name="guests-group-update-retrieve"),
    path("groups/delete/<str:pk>/", GuestGroupDeleteAPIView.as_view(), name="guests-group-delete"),
]