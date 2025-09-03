from django.contrib import admin

from apps.guests.models import Guest


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("hotel", "gender", "full_name", "price")
    list_display_links = list_display
    search_fields = ("hotel", "full_name")
    list_filter = ("hotel", "gender")