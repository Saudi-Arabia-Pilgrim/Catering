from django.urls import path

from apps.rooms.views.rooms import (RoomTypeListAPIView,
                                    RoomTypeCreateAPIView,
                                    RoomTypeRetrieveAPIView,
                                    RoomTypeUpdateAPIView,
                                    RoomTypeDeleteAPIView)


urlpatterns = [
    path("", RoomTypeListAPIView.as_view(), name="rooms"),

    # ================ CRUD OF ROOM_TYPE ====================
    path("create/", RoomTypeCreateAPIView.as_view(), name="create_room_type"),
    path("<str:pk>/", RoomTypeRetrieveAPIView.as_view(), name="retrieve_room_type"),
    path("update/<str:pk>/", RoomTypeUpdateAPIView.as_view(), name="update_room_type"),
    path("delete/<str:pk>/", RoomTypeDeleteAPIView.as_view(), name="delete_room_type"),
]