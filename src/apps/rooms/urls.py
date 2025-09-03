from django.urls import path

from apps.rooms.views.room_of_hotel import (RoomListsAPIView,
                                            RoomCreateAPIView,
                                            RoomRetrieveAPIView,
                                            RoomUpdateAPIView,
                                            RoomDeleteAPIView)

from apps.rooms.views.room_types import (RoomTypeListsAPIView,
                                         RoomTypeCreateAPIView,
                                         RoomTypeRetrieveAPIView,
                                         RoomTypeUpdateAPIView,
                                         RoomTypeDeleteAPIView)
from apps.rooms.views.rooms_group_delete import RoomGroupDeleteAPIView
from apps.rooms.views.rooms_on_hotel import RoomsOfHotelAPIView


urlpatterns = [
    # ================== Room Types ===========================
    path("room_types/", RoomTypeListsAPIView.as_view(), name="room_type_list"),
    path("room_type/create/", RoomTypeCreateAPIView.as_view(), name="room_type_create"),
    path("room_type/<str:pk>/", RoomTypeRetrieveAPIView.as_view(), name="room_type_retrieve"),
    path("room_type/update/<str:pk>/", RoomTypeUpdateAPIView.as_view(), name="room_type_update"),
    path("room_type/delete/<str:pk>/", RoomTypeDeleteAPIView.as_view(), name="room_type_delete"),

    # ================== Rooms of Hotels ===========================
    path("", RoomListsAPIView.as_view(), name="room_list"),
    path("create/", RoomCreateAPIView.as_view(), name="room_create"),
    path("<str:pk>/", RoomRetrieveAPIView.as_view(), name="room_retrieve"),
    path("update/<str:pk>/", RoomUpdateAPIView.as_view(), name="room_update"),
    path("delete/<uuid:pk>/", RoomDeleteAPIView.as_view(), name="room_delete"),

    path("rooms_of_hotel/<str:pk>/", RoomsOfHotelAPIView.as_view(), name="room_list_of_hotel"),
    path("delete/group/", RoomGroupDeleteAPIView.as_view(), name="room_group_delete"),
]
