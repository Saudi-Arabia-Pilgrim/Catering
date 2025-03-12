from django.db import models

from apps.base.models import AbstractBaseModel


class Warehouse(AbstractBaseModel):
    """
    Warehouse model that represents the storage details of products.
    """

    # === Foreign key to the Product model, representing the product stored in the warehouse. ===
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        related_name='warehouses')
    # === The name of the warehouse. ===
    name = models.CharField(max_length=255)
    # === A unique slug for the warehouse. ===
    slug = models.SlugField(max_length=255, unique=True)
    # === The status of the warehouse, indicating if it is active. ===
    status = models.BooleanField(default=True)
    # === The gross price of the product in the warehouse. ===
    gross_price = models.DecimalField(max_digits=10, decimal_places=2)
    # === The count of products available in the warehouse. ===
    count = models.PositiveIntegerField()
    # === The net price of the product in the warehouse. ===
    net_price = models.DecimalField(max_digits=10, decimal_places=2)


    class Meta:
        # === The name of the database table. ===
        db_table = 'warehouse'
        # === The singular name for the warehouse. ===
        verbose_name = 'Warehouse'
        # === The plural name for the warehouse. ===
        verbose_name_plural = 'Warehouses'

    def __str__(self):
        """
        Returns the name of the warehouse.
        """
        return self.name