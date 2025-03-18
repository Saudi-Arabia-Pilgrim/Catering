from django.contrib import admin

from apps.rooms.models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "hotel",
        "room_type",
        "capacity",
        "status",
        "count",
        "occupied_count",
        "net_price",
        "profit",
        "gross_price",
    )
    list_display_links = list_display
    list_filter = ("hotel", "room_type")