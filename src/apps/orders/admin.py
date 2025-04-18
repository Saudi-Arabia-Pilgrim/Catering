from django.contrib import admin

from apps.orders.models import FoodOrder, HotelOrder

admin.site.register(FoodOrder)

admin.site.register(HotelOrder)
