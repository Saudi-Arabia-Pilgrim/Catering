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
    room_type = models.ForeignKey(
        "rooms.RoomType",
        on_delete=models.CASCADE,
        related_name="rooms",
        help_text="Reference to the type of room (e.g., Single, Double, Suite)."
    )
    count = models.PositiveSmallIntegerField(
        help_text="Total number of rooms available of this type in the hotel."
    )
    occupied_count = models.PositiveSmallIntegerField(
        default=0,
        help_text="Number of currently occupied rooms. Defaults to 0."
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price per night for the room type."
    )

    @property
    def available_count(self):
        """
        Calculates the number of available rooms of this type.

        Returns:
            int: The number of available rooms. Ensures non-negative values.
        """
        return self.count - self.occupied_count if self.count >= self.occupied_count else 0