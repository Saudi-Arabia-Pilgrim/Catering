from math import ceil

from django.db import models
from django.db.models import Sum
from django.utils import timezone

from apps.guests.models import Guest
from apps.base.models import AbstractBaseModel
from apps.base.exceptions import CustomExceptionError
from apps.orders.utils.refresh_rooms import update_room_occupancy


class RoomQuerySet(models.QuerySet):
    def available(self):
        return self.filter(is_busy=False)


class Room(AbstractBaseModel):
    """
    Model representing a room in a hotel.

    Attributes:
        hotel (ForeignKey): Reference to the hotel the room belongs to.
        room_type (ForeignKey): Reference to the type of room (e.g., Single, Double, Suite).
        count (PositiveSmallIntegerField): Total number of rooms available of this type in the hotel.
        occupied_count (PositiveSmallIntegerField): Number of currently occupied rooms. Defaults to 0.
        price (DecimalField): Price per night for the room type.
    """

    objects = RoomQuerySet.as_manager()

    hotel = models.ForeignKey(
        "hotels.Hotel",
        on_delete=models.CASCADE,
        related_name="rooms",
        help_text="Reference to the hotel the room belongs to."
    )
    # ========== for room_type ============
    room_type = models.ForeignKey(
        "rooms.RoomType",
        on_delete=models.PROTECT,
        related_name="rooms"
    )

    count = models.PositiveSmallIntegerField()

    capacity = models.PositiveSmallIntegerField(
        help_text="The maximum number of guests that can stay in a room of this type."
    )

    floor = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="Etaj (qavat) raqami",
    )

    room_number = models.CharField(
        max_length=10,
        blank=True,
        help_text="Xona raqami, masalan 101, 205",
    )

    remaining_capacity = models.PositiveSmallIntegerField(default=0)

    # =============   end room_type   =================

    available_count = models.PositiveSmallIntegerField(default=0)

    occupied_count = models.PositiveSmallIntegerField(
        default=0,
        help_text="Number of currently occupied rooms. Defaults to 0."
    )
    net_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price per night for the room type."
    )
    profit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price per night for the room type."
    )
    gross_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        help_text="Price per night for the room type."
    )
    is_busy = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    @property
    def current_occupied_count(self):
        return Guest.objects.filter(room=self, status=Guest.Status.COMPLETED).count()

    @classmethod
    def remaining_capacity_calculated(cls, rooms):
        today = timezone.now().date()

        active_guests_count = Guest.objects.filter(
            room__in=rooms,
            status=Guest.Status.NEW,
            check_in__lte=today,
            check_out__gte=today
        ).aggregate(total=Sum("count"))["total"] or 0

        total_capacity = rooms.aggregate(capacity=Sum("capacity"))["capacity"] or 0

        remaining_capacity = total_capacity - active_guests_count
        return remaining_capacity

    def apply_save_logic(self):

        if self.net_price is not None and self.profit is not None:
            self.gross_price = self.net_price + self.profit


    def save(self, *args, **kwargs):
        self.apply_save_logic()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.room_number}"
