from django.db import models
from django.utils.text import slugify

from apps.base.models import AbstractBaseModel
from apps.warehouses.models import Warehouse


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
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    # === An optional image of the product, with the upload path 'products/%Y/%m/%d/'. ===
    image = models.ImageField(upload_to='products/%Y/%m/%d/', null=True, blank=True)
    # === The status of the product, indicating if it is active (default is True). ===
    status = models.BooleanField(default=False)

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

    def clean(self):
        """
        Cleans the product instance by generating a slug from the product name.

        This method uses the `slugify` function to convert the product name into a URL-friendly slug and assigns it to the `slug` attribute of the product instance.
        """
        self.slug = slugify(self.name)