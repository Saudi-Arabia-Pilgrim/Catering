from django.db import models

from apps.base.models import AbstractBaseModel


class Product(AbstractBaseModel):
    """
    Represents a product in the catering application.
    """

    # === A foreign key to the Measure model, representing the unit of measurement for the product. ===
    measure = models.ForeignKey('sections.Measure', on_delete=models.PROTECT, related_name='products')
    # === A foreign key to the Section model, representing the section/category of the product. ===
    section = models.ForeignKey('sections.Section', on_delete=models.PROTECT, related_name='products')
    # === The name of the product. ===
    name = models.CharField(max_length=255)
    # === A unique slug for the product. ===
    slug = models.SlugField(max_length=255, unique=True)
    # === An optional image of the product, with the upload path 'products/%Y/%m/%d/'. ===
    image = models.ImageField(upload_to='products/%Y/%m/%d/', null=True, blank=True)
    # === The status of the product, indicating if it is active (default is True). ===
    status = models.BooleanField(default=True)
    # === The price of the product, with a maximum of 10 digits and 2 decimal places. ===
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        # === The name of the database table ('product'). ===
        db_table = 'product'
        # === The human-readable singular name of the model. ===
        verbose_name = 'Product'
        # === The human-readable plural name of the model. ===
        verbose_name_plural = 'Products'

    def __str__(self):
        """
        Returns the string representation of the product, which is its name.
        """
        return self.name