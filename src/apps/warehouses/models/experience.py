from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

from apps.base.models import AbstractBaseModel


class Experience(AbstractBaseModel):
    warehouse = models.ForeignKey("warehouses.Warehouse", on_delete=models.PROTECT, related_name="experiences")
    count = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.count

    class Meta:
        db_table = "experience"
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"
        # === Ordering field for sorting a set of queries ===
        ordering = ["-created_at"]
