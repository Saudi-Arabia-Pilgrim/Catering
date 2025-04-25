
from django.db import models
from django.utils.text import slugify

from apps.base.models import AbstractBaseModel


class Transport(AbstractBaseModel):
    """
    Transport model for managing transportation details.
    """
    name = models.CharField(max_length=255, help_text="Name of the transport")
    slug = models.SlugField(max_length=255, unique=True, help_text="Unique slug for the transport", blank=True)
    name_of_driver = models.CharField(max_length=255, help_text="Name of the driver")
    address = models.CharField(max_length=255, help_text="Nearby address of the transport")
    phone_number = models.CharField(max_length=20, help_text="Phone number of the driver or transport company")
    amount_of_people = models.CharField(max_length=50, help_text="Maximum number of people the transport can accommodate")
    status = models.BooleanField(default=True, help_text="Status of the transport (active/inactive)")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Transport"
        verbose_name_plural = "Transports"
        ordering = ["-created_at"]
