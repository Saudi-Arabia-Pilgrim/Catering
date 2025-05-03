from django.db import models

from apps.base.models import AbstractBaseModel


class Experience(AbstractBaseModel):
    warehouse = models.ForeignKey("warehouses.Warehouse", on_delete=models.PROTECT, related_name="experiences")
    count = models.CharField(max_length=10)
    price = models.FloatField()

    def __str__(self):
        return self.count

    class Meta:
        db_table = "experience"
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"