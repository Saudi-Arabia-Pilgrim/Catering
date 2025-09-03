from django.contrib import admin

from apps.hotels.models import Hotel


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "address", "email", "phone_number", "rating")
    list_display_links = list_display
    search_fields = ("name", "slug", "address", "email", "phone_number")
    prepopulated_fields = {"slug": ("name",)}