from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

from apps.base.models import AbstractBaseModel
from apps.warehouses.utils.generate_id import new_id


class Warehouse(AbstractBaseModel):
    """
    Warehouse model that represents the storage details of products.
    """

    # === Foreign key to the Product model, representing the product stored in the warehouse. ===
    product = models.ForeignKey(
        "products.Product", on_delete=models.PROTECT, related_name="warehouses"
    )
    # === The status of the warehouse, indicating if it is active. ===
    status = models.BooleanField(default=True)
    # === The gross price of the product in the warehouse. ===
    gross_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(1)]
    )
    # === The count of products available in the warehouse. ===
    count = models.FloatField(default=0, validators=[MinValueValidator(0)])
    # === The count of products that have arrived in the warehouse. ===
    arrived_count = models.FloatField(validators=[MinValueValidator(1)])

    class Meta:
        # === The name of the database table. ===
        db_table = "warehouse"
        # === The singular name for the warehouse. ===
        verbose_name = "Warehouse"
        # === The plural name for the warehouse. ===
        verbose_name_plural = "Warehouses"
        # === Ordering field for sorting a set of queries ===
        ordering = ["-created_at"]

    def __str__(self):
        """
        Returns the name of the warehouse.
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        Override the save method to perform custom actions before saving the model instance.

        This method performs the following actions:
        1. If the count is 0 and the status is True, set the status to False.
        2. Calculate the net price by dividing the gross price by the count.
        3. Generate a slug from the name if the slug is not set or does not match the slugified name.
        4. If the count is not set, assign it the value of arrived_count.

        Returns:
            None
        """
        if self.count == 0 and not self._state.adding:
            self.status = False
        elif self.count > 0:
            self.status = True
        else:
            self.count = self.arrived_count
            self.status = True
        super().save(*args, **kwargs)

    def get_net_price(self):
        measure = self.product.difference_measures
        if not measure:
            measure = 1

        return float(self.gross_price / Decimal(self.arrived_count * measure))
