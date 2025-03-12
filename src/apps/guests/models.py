import random

from django.db import models

from apps.base.models import AbstractBaseModel

class Guest(AbstractBaseModel):
    """
    Model representing a guest staying at a hotel.

    Attributes:
        hotel (ForeignKey): The hotel where the guest is staying.
        gender (PositiveSmallIntegerField): The gender of the guest, chosen from predefined options.
        full_name (CharField): The full name of the guest.
        price (DecimalField): The price associated with the guest's stay.
    """

    class Gender(models.IntegerChoices):
        """
        Enumeration for guest gender choices.
        """
        MALE = 1, 'Male'
        FEMALE = 2, 'Female'

    hotel = models.ForeignKey(
        'hotels.Hotel',
        on_delete=models.CASCADE,
        related_name='guests',
        help_text="The hotel where the guest is staying."
    )
    hotel_order = models.ForeignKey(
        'orders.HotelOrder',
        on_delete=models.PROTECT,
        related_name='guests',
        help_text="The hotel order associated with the guest."
    )
    room_type = models.ForeignKey(
        "rooms.RoomType",
        on_delete=models.CASCADE,
        related_name="guests",
        help_text="The type of room the guest is staying in."
    )
    order_number = models.CharField(
        max_length=8,
        unique=True,
        editable=False,
    )

    gender = models.PositiveSmallIntegerField(
        choices=Gender.choices,
        help_text="Gender of the guest (Male or Female)."
    )
    full_name = models.CharField(
        max_length=255,
        help_text="Full name of the guest."
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price associated with the guest's stay."
    )
    check_in = models.DateField(
        help_text="Date of check-in."
    )
    check_out = models.DateField(
        help_text="Date of check-out."
    )

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"№{random.randint(1000000, 9999999)}"
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return a string representation of the guest, which is the full name.
        """
        return self.full_name
