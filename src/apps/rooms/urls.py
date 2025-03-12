from django.urls import path

from apps.rooms.views.rooms import (RoomTypeListAPIView,
                                    RoomTypeCreateAPIView,
                                    RoomTypeRetrieveAPIView,
                                    RoomTypeUpdateAPIView,
                                    RoomTypeDeleteAPIView)
from apps.rooms.views.rooms_of_hotel import (RoomsOfHotelListAPIView,
                                             RoomOfHotelCreateAPIView,
                                             RoomOfHotelRetrieveAPIView,
                                             RoomOfHotelUpdateAPIView,
                                             RoomOfHotelDeleteAPIView)

urlpatterns = [
    # ================ List of RoomType ====================
    path("room_types/", RoomTypeListAPIView.as_view(), name="rooms"),

    # ================ CRUD OF ROOM_TYPE ====================
    path("room_types/create/", RoomTypeCreateAPIView.as_view(), name="create_room_type"),
    path("room_types/<str:pk>/", RoomTypeRetrieveAPIView.as_view(), name="retrieve_room_type"),
    path("room_types/update/<str:pk>/", RoomTypeUpdateAPIView.as_view(), name="update_room_type"),
    path("room_types/delete/<str:pk>/", RoomTypeDeleteAPIView.as_view(), name="delete_room_type"),

    # ================ List of RoomType ====================
    path("", RoomsOfHotelListAPIView.as_view(), name="rooms_of_hotel"),

    # ================ CRUD OF Room to Hotel ====================
    path("create/", RoomOfHotelCreateAPIView.as_view(), name="create_room_of_hotel"),
    path("<str:pk>/", RoomOfHotelRetrieveAPIView.as_view(), name="retrieve_room_of_hotel"),
    path("update/<str:pk>/", RoomOfHotelUpdateAPIView.as_view(), name="update_room_of_hotel"),
    path("delete/<str:pk>/", RoomOfHotelDeleteAPIView.as_view(), name="delete_room_of_hotel"),
]
