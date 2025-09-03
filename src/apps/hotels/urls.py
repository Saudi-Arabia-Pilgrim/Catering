from django.urls import path

from apps.hotels.views.hotels import HotelListAPIView
from apps.hotels.views import (HotelCreateAPIView,
                               HotelRetrieveAPIView,
                               HotelUpdateAPIView,
                               HotelDeleteAPIView)


urlpatterns = [
    path("", HotelListAPIView.as_view(), name="hotels"),

    # ============= CRUD OF HOTEL =================
    path("create/", HotelCreateAPIView.as_view(), name="create_hotel"),
    path("<str:pk>/", HotelRetrieveAPIView.as_view(), name="retrieve_hotel"),
    path("update/<str:pk>/", HotelUpdateAPIView.as_view(), name="update_hotel"),
    path("delete/<str:pk>/", HotelDeleteAPIView.as_view(), name="delete_hotel"),

]