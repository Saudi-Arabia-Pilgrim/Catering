from django.db import models
from django.utils.text import slugify

from apps.base.models import AbstractBaseModel


class Section(AbstractBaseModel):
    """
    Model representing a Section.
    """
    # === The name of the section. ===
    name = models.CharField(max_length=64)
    # === A unique slug for the section. ===
    slug = models.SlugField(max_length=64, unique=True, blank=True)

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
    
    def clean(self):
        """
        Override the clean method to automatically generate and set the slug
        field based on the name field if it is not already set or if it does
        not match the slugified version of the name.

        This method is called by Django's full_clean method, which is typically
        called before saving a model instance.

        Returns:
            None
        """
        self.slug = slugify(self.name)