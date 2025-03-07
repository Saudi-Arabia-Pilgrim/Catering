from django.db import models

from apps.base.models import AbstractBaseModel


class Section(AbstractBaseModel):
    """
    Model representing a Section.
    """
    # === The name of the section. ===
    name = models.CharField(max_length=64)
    # === A unique slug for the section. ===
    slug = models.SlugField(max_length=64, unique=True)

    class Meta:
        # === The name of the database table. ===
        db_table = 'section'
        # === The human-readable name of the model. ===
        verbose_name = 'Section'
        # === The human-readable plural name of the model. ===
        verbose_name_plural = 'Sections'

    def __str__(self):
        """
        Returns the string representation of the section, which is its name.
        """
        return self.name