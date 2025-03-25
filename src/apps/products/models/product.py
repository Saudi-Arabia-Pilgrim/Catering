from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator

from apps.base.exceptions import CustomExceptionError
from apps.base.models import AbstractBaseModel


class Product(AbstractBaseModel):
    """
    Represents a product in the catering application.
    """

    # === A foreign key to the Measure model, representing the unit of measurement for the product. ===
    measure = models.ForeignKey('sections.Measure', on_delete=models.PROTECT, related_name='products')
    # === A foreign key to the Measure model representing the unit of measure of a product in warehouse. ===
    measure_warehouse = models.ForeignKey('sections.Measure', on_delete=models.PROTECT, related_name='products_warehouse')
    # === The difference between the measures ===
    difference_measures = models.FloatField(validators=[MinValueValidator(0)])
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

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        obj = self.__class__.objects.filter(slug=slug).exclude(pk=self.pk).first()
        if obj:
            raise CustomExceptionError(code=400, detail="A product with this name already exists")
        self.slug = slug
        return super().save(*args, **kwargs)