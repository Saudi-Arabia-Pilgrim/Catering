from django.urls import path

from apps.rooms.views.room_lists import (RoomListsAPIView,
                                         RoomCreateAPIView,
                                         RoomRetrieveAPIView,
                                         RoomUpdateAPIView,
                                         RoomDeleteAPIView)


urlpatterns = [
    path("", RoomListsAPIView.as_view(), name="room_list"),
    path("create/", RoomCreateAPIView.as_view(), name="room_create"),
    path("<str:pk>/", RoomRetrieveAPIView.as_view(), name="room_retrieve"),
    path("update/<str:pk>/", RoomUpdateAPIView.as_view(), name="room_update"),
    path("delete/<str:pk>/", RoomDeleteAPIView.as_view(), name="room_delete"),
]