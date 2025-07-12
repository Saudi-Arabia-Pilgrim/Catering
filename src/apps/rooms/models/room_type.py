from django.db import models
from django.utils.text import slugify

from apps.base.models import AbstractBaseModel


class RoomType(AbstractBaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    status = models.BooleanField(
        default=True,
        help_text="Indicates whether the room type is active or not."
    )

    class Meta:
        ordering = ["-created_at"]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name