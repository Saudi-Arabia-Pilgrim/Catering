from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator

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
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    # === The status of the warehouse, indicating if it is active. ===
    status = models.BooleanField(default=True)
    # === The gross price of the product in the warehouse. ===
    gross_price = models.DecimalField(max_digits=10,
                                      decimal_places=2,
                                      validators=[MinValueValidator(1)])
    # === The count of products available in the warehouse. ===
    count = models.FloatField(validators=[MinValueValidator(0)], blank=True)
    # === The count of products that have arrived in the warehouse. ===
    arrived_count = models.FloatField(validators=[MinValueValidator(1)])
    # === The net price of the product in the warehouse. ===
    net_price = models.DecimalField(max_digits=10,
                                    decimal_places=2,
                                    validators=[MinValueValidator(1)],
                                    blank=True)

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

    def clean(self):
        """
        Override the clean method to perform custom actions before validating the model instance.

        This method performs the following actions:
        1. If the count is 0 and the status is True, set the status to False.
        2. Calculate the net price by dividing the gross price by the count.
        3. Generate a slug from the name if the slug is not set or does not match the slugified name.
        4. If the count is not set, assign it the value of arrived_count.

        Returns:
            None
        """
        if self.count == 0 and self.status:
            self.status = False

        self.net_price = self.gross_price / self.count
        
        self.slug = slugify(self.name)

        if not self.count:
            self.count = self.arrived_count