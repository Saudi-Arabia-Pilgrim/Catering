from django.contrib import admin

from apps.menus.models import Menu, Recipe


admin.site.register(Menu)
admin.site.register(Recipe)