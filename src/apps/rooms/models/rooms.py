from django.db.models import Sum
from django.utils import timezone

from django.db import models

from apps.base.exceptions import CustomExceptionError
from apps.base.models import AbstractBaseModel
from apps.guests.models import Guest


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

    hotel = models.ForeignKey(
        "hotels.Hotel",
        on_delete=models.PROTECT,
        related_name="rooms",
        help_text="Reference to the hotel the room belongs to."
    )
    # ========== for room_type ============
    room_type = models.ForeignKey(
        "rooms.RoomType",
        on_delete=models.PROTECT,
        related_name="rooms"
    )

    capacity = models.PositiveSmallIntegerField(
        help_text="The maximum number of guests that can stay in a room of this type."
    )

    # =============   end room_type   =================

    available_count = models.PositiveSmallIntegerField(default=0)
    remaining_capacity = models.PositiveSmallIntegerField(default=0)

    is_fully_occupied = models.BooleanField(default=False,
                                            help_text="True if all available guest capacity has been filled.")

    count = models.PositiveSmallIntegerField(
        help_text="Total number of rooms available of this type in the hotel."
    )
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

    @property
    def current_occupied_count(self):
        return Guest.objects.filter(room=self, status=Guest.Status.COMPLETED).count()

    def refresh_occupancy(self):
        today = timezone.now().date()

        active_guests = Guest.objects.filter(
            room=self,
            status=Guest.Status.NEW,
            check_in__lte=today,
            check_out__gte=today
        ).aggregate(total=Sum("count"))

        total_people = active_guests["total"] or 0

        occupied_rooms = total_people // self.capacity
        if total_people % self.capacity:
            occupied_rooms += 1

        self.occupied_count = min(occupied_rooms, self.count)
        self.available_count = max(self.count - self.occupied_count, 0)
        self.remaining_capacity = max((self.count * self.capacity) - total_people, 0)
        self.is_fully_occupied = self.occupied_count >= self.count

    def clean(self):
        if self.count < self.occupied_count:
            raise CustomExceptionError(code=400, detail="Occupied count cannot be greater than total room count.")
        if self.count < 0:
            raise CustomExceptionError(code=400, detail="Room count must be non-negative.")

    def save(self, *args, **kwargs):
        self.refresh_occupancy()

        self.net_price = self.net_price or 0
        self.profit = self.profit or 0
        self.gross_price = self.net_price + self.profit

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.gross_price}"
