from django.contrib import admin

from apps.warehouses.models import Warehouse, ProductsUsed, Experience


admin.site.register(Warehouse)
admin.site.register(ProductsUsed)
admin.site.register(Experience)
