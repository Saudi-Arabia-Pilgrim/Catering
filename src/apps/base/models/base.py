import uuid

from django.conf import settings
from django.db import models

from apps.base.services import normalize_text_fields

class AbstractBaseModel(models.Model):
    """Abstract base model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        editable=False,
        related_name="%(app_label)s_%(class)s_set",
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        editable=False,
        related_name="%(app_label)s_%(class)s_updated",
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        auto_now=True,
        editable=False,
    )
    deleted_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        editable=False,
        related_name="%(app_label)s_%(class)s_deleted",
    )

    def save(self, *args, **kwargs):
        """
        Normalize text fields before saving.
        :param args:
        :param kwargs:
        :return: None
        """
        normalize_text_fields(self)
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True