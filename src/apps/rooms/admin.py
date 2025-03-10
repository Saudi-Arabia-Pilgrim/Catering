from django.contrib import admin

from apps.rooms.models import Room, RoomType


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("hotel", "room_type", "count", "occupied_count", "price")
    list_display_links = list_display
    list_filter = ("hotel", "room_type")


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    list_display_links = list_display
