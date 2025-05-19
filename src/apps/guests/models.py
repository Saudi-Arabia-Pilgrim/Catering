import random

from django.db import models
from django.db.models import Sum
from django.utils.timezone import now

from apps.base.models import AbstractBaseModel
from apps.base.exceptions import CustomExceptionError


class Guest(AbstractBaseModel):
    """
    Model representing a guest staying at a hotel.

    Attributes:
        hotel (ForeignKey): The hotel where the guest is staying.
        gender (PositiveSmallIntegerField): The gender of the guest, chosen from predefined options.
        full_name (CharField): The full name of the guest.
        price (DecimalField): The price associated with the guest's stay.
    """
    class Status(models.TextChoices):
        NEW = "New"
        COMPLETED = "Completed"
        CANCELED = "Canceled"

    class Gender(models.IntegerChoices):
        """
        Enumeration for guest gender choices.
        """
        MALE = 1, 'Male'
        FEMALE = 2, 'Female'

    hotel = models.ForeignKey(
        'hotels.Hotel',
        on_delete=models.PROTECT,
        related_name='guests',
        help_text="The hotel where the guest is staying."
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.PROTECT,
        related_name="guests",
        help_text="The type of room the guest is staying in."
    )

    status = models.CharField(choices=Status.choices, max_length=30, default=Status.NEW)

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
    count = models.PositiveSmallIntegerField(
        default=1,
        help_text="Number of people represented by this guest record (usually 1, but can be more for group bookings)."
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        editable=False,
        help_text="Price associated with the guest's stay."
    )
    check_in = models.DateField(
        help_text="Date of check-in."
    )
    check_out = models.DateField(
        help_text="Date of check-out."
    )

    def clean(self):
        today = now().date()

        if self.check_out <= self.check_in:
            raise CustomExceptionError(code=400, detail="Check-out check-in dan keyin bo‘lishi kerak.")

        if self.count > self.room.capacity:
            raise CustomExceptionError(code=400, detail=f"Bu xonaga {self.room.capacity} tadan ko‘p odam joylasholmaydi.")

        needed_rooms = self.count // self.room.capacity
        if self.count % self.room.capacity:
            needed_rooms += 1

        active_guests = Guest.objects.filter(
            room=self.room,
            status=Guest.Status.NEW,
            check_in__lte=today,
            check_out__gte=today
        )

        if self.pk:
            active_guests = active_guests.exclude(pk=self.pk)

        total_people = active_guests.aggregate(total=Sum("count"))["total"] or 0

        occupied_rooms = total_people // self.room.capacity
        if total_people % self.room.capacity:
            occupied_rooms += 1

        # available_rooms = self.room.count - occupied_rooms

        # if needed_rooms > available_rooms:
        #     raise CustomExceptionError(code=400, detail=f"{available_rooms} ta xona qolgan xolos. {needed_rooms} ta kerak.")


    def save(self, *args, **kwargs):
        if self.pk:
            existing = Guest.objects.filter(pk=self.pk).first()
            if existing and existing.status == Guest.Status.COMPLETED:
                raise CustomExceptionError(code=400, detail="Tugatildigan mehmonni o‘zgartirib bo‘lmaydi.")

        if not self.order_number:
            self.order_number = f"№{random.randint(1000000, 9999999)}"

        room = self.room

        self.full_clean()
        super().save(*args, **kwargs)
        room.refresh_occupancy()

        if self.status == Guest.Status.COMPLETED:
            room.refresh_occupancy()

    def delete(self, *args, **kwargs):
        room = self.room
        super().delete(*args, **kwargs)
        room.refresh_occupancy()

    def __str__(self):
        """
        Return a string representation of the guest, which is the full name.
        """
        return self.full_name
