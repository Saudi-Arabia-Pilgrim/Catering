from django.contrib import admin

from apps.warehouses.models import Warehouse, ProductsUsed


admin.site.register(Warehouse)
admin.site.register(ProductsUsed)
