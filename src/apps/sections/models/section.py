from django.db import models
from django.utils.text import slugify

from apps.base.exceptions import CustomExceptionError
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
        db_table = "section"
        # === The human-readable name of the model. ===
        verbose_name = "Section"
        # === The human-readable plural name of the model. ===
        verbose_name_plural = "Sections"

    def __str__(self):
        """
        Returns the string representation of the section, which is its name.
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        Override the save method to automatically generate and set the slug
        field based on the name field if it is not already set or if it does
        not match the slugified version of the name.

        This method is called before saving a model instance.

        Returns:
            None
        """
        slug = slugify(self.name)
        obj = self.__class__.objects.filter(slug=slug).exclude(pk=self.pk).first()
        if obj:
            raise CustomExceptionError(
                code=400, detail="A section with this name already exists"
            )
        self.slug = slug
        super().save(*args, **kwargs)
