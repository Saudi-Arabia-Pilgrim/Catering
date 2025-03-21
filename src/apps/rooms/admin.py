from django.contrib import admin

from apps.rooms.models.rooms import Room
from apps.rooms.models.room_type import RoomType


@admin.register(RoomType)
class RoomType(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "status"
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hotel",
        "room_type",
        "capacity",
        "count",
        "occupied_count",
        "net_price",
        "profit",
        "gross_price",
    )
    list_display_links = list_display
    list_filter = ("hotel", "room_type")
