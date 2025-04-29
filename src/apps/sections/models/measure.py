from django.db import models
from django.utils.text import slugify

from apps.base.exceptions import CustomExceptionError
from apps.base.models import AbstractBaseModel


class Measure(AbstractBaseModel):
    """
    Model representing a measurement unit.
    """

    # === The name of the measurement unit. ===
    name = models.CharField(max_length=64)
    # === Unique slug for the measure ===
    slug = models.SlugField(max_length=64, unique=True, blank=True)
    # === Abbreviation name of the measure ===
    abbreviation = models.CharField(max_length=8)
    # === The status of the measure ===
    status = models.BooleanField(default=True)

    class Meta:
        # === The name of the database table. ===
        db_table = "measure"
        # === The human-readable name of the model. ===
        verbose_name = "Measure"
        # === The plural form of the human-readable name of the model. ===
        verbose_name_plural = "Measures"

    def __str__(self):
        """
        Returns the string representation of the measurement unit.
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        Override the save method to automatically generate and set the slug
        field based on the name field if it is not already set or if it does
        not match the slugified version of the name.
        """
        slug = slugify(self.name)
        obj = self.__class__.objects.filter(slug=slug).exclude(pk=self.pk).first()
        if obj:
            raise CustomExceptionError(
                code=400, detail="A product with this name already exists"
            )
        self.slug = slug
        super().save(*args, **kwargs)
