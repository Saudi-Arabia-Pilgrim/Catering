from django.db import models

from apps.base.models import AbstractBaseModel


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
        on_delete=models.CASCADE,
        related_name="rooms",
        help_text="Reference to the hotel the room belongs to."
    )
    # ========== for room_type ============
    room_type = models.ForeignKey(
        "rooms.RoomType",
        on_delete=models.CASCADE,
        related_name="rooms"
    )

    capacity = models.PositiveSmallIntegerField(
        help_text="The maximum number of guests that can stay in a room of this type."
    )

    # =============   end room_type   =================

    count = models.PositiveSmallIntegerField(
        help_text="Total number of rooms available of this type in the hotel."
    )
    occupied_count = models.PositiveSmallIntegerField(
        default=0,
        help_text="Number of currently occupied rooms. Defaults to 0."
    )
    partial_occupied_count = models.PositiveSmallIntegerField(default=0,
        help_text="Number of guests in the currently partially occupied room, if any."
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
    def available_count(self):
        """
        Fizik xonalar soni:
          count - (occupied_count + (1 if partial room exists else 0))
        Agar partial xona mavjud bo‘lsa, u yangi buyurtma uchun ham ishlatiladi,
        ammo shu xona alohida yangi band xona sifatida hisoblanmaydi.
        """
        partial_room = 1 if self.partial_occupied_count > 0 else 0
        return max(self.count - self.occupied_count - partial_room, 0)

    def save(self, *args, **kwargs):
        self.net_price = self.net_price or 0
        self.profit = self.profit or 0
        self.gross_price = self.net_price + self.profit
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.gross_price}"
