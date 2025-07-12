from django.db import models

from apps.base.models import AbstractBaseModel


class RoomType(AbstractBaseModel):
    name = models.CharField(max_length=255)
    status = models.BooleanField(
        default=True,
        help_text="Indicates whether the room type is active or not."
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name