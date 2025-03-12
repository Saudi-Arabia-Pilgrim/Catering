from django.db import models

from apps.base.models import AbstractBaseModel

class RoomType(AbstractBaseModel):
    """
    Model representing different types of rooms available in a hotel.

    Attributes:
        name (CharField): The name of the room type (e.g., Single, Double, Suite).
        status (BooleanField): Indicates whether the room type is active or not.
    """

    name = models.CharField(
        max_length=255,
        help_text="The name of the room type (e.g., Single, Double, Suite)."
    )
    status = models.BooleanField(
        default=True,
        help_text="Indicates whether the room type is active or not."
    )

    def __str__(self):
        """
        Returns the string representation of the room type.

        Returns:
            str: The name of the room type.
        """
        return self.name