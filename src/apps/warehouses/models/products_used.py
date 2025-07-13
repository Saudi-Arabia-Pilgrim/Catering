from django.db import models

from apps.base.models.base import AbstractBaseModel


class ProductsUsed(AbstractBaseModel):
    order_id = models.CharField(max_length=24, db_index=True, default="0")
    warehouse = models.ForeignKey("warehouses.Warehouse", on_delete=models.PROTECT, related_name="used")
    count = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.count

    class Meta:
        db_table = "used_products"
        verbose_name = "Used"
        verbose_name_plural = "UsedProducts"
        # === Ordering field for sorting a set of queries ===
        ordering = ["-created_at"]
