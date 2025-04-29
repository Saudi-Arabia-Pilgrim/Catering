from django.db import models

from apps.base.models.base import AbstractBaseModel


class ProductsUsed(AbstractBaseModel):
    warehouse = models.ForeignKey("warehouses.Warehouse", on_delete=models.PROTECT, related_name="used")
    count = models.CharField(max_length=10)
    price = models.FloatField()

    def __str__(self):
        return self.count
    
    class Meta:
        db_table = "used_products"
        verbose_name = "Used"
        verbose_name_plural = "UsedProducts"