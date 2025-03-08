from django.db import models

from apps.base.models import AbstractBaseModel


class Measure(AbstractBaseModel):
    """
    Model representing a measurement unit.
    """
    # === The name of the measurement unit. ===
    name = models.CharField(max_length=64)
    # === Unique slug for the measure ===
    slug = models.SlugField(max_length=64, unique=True)
    # === Abbreviation name of the measure === 
    abbreviation = models.CharField(max_length=8)

    class Meta:
        # === The name of the database table. ===
        db_table = 'measure'
        # === The human-readable name of the model. ===
        verbose_name = 'Measure'
        # === The plural form of the human-readable name of the model. ===
        verbose_name_plural = 'Measures'

    def __str__(self):
        """
        Returns the string representation of the measurement unit.
        """
        return self.name