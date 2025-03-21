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
    path("delete/<str:pk>/", RoomDeleteAPIView.as_view(), name="room_delete"),
]
