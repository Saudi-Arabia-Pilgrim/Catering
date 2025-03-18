from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils.text import slugify

from apps.base.models import AbstractBaseModel


class Hotel(AbstractBaseModel):
    """
    Model representing a hotel.

    Attributes:
        name (CharField): The name of the hotel.
        slug (SlugField): A unique slug identifier for the hotel.
        address (CharField): The physical address of the hotel.
        email (EmailField): A unique email contact for the hotel.
        phone_number (CharField): The contact phone number with validation for Saudi Arabia format.
        rating (DecimalField): The hotel's rating, restricted between 0.00 and 5.00.
    """

    name = models.CharField(
        max_length=255,
        help_text="The name of the hotel."
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text="A unique slug identifier for the hotel."
    )
    address = models.CharField(
        max_length=255,
        help_text="The physical address of the hotel."
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        help_text="A unique email contact for the hotel."
    )
    phone_number = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r"^\+966\d{10}$",
                message="Example: +966 011 XXX XXXX",
            )
        ],
        help_text="The contact phone number (e.g., +966 011 XXX XXXX)."
    )
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10)],
        help_text="The hotel's rating, between 0.00 and 5.00."
    )

    def clean(self):
        self.slug = slugify(self.name)

    def __str__(self):
        """
        Return a string representation of the hotel, which is its name.
        """
        return self.name
