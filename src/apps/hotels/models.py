from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models

from apps.base.models import AbstractBaseModel


class Hotel(AbstractBaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r"^\+966\d{10}$",
                message="Example: +966 011 XXX XXXX",
            )])
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.00), MaxValueValidator(5.00)],
    )

    def __str__(self):
        return self.name