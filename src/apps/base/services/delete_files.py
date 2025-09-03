import logging
from typing import Type, Tuple

from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import FileField, ImageField, Model

logger = logging.getLogger(__name__)

def delete_file_after_object_deletion(
    instance: Model,
    field_types: Tuple[Type[FileField], ...] = (FileField, ImageField)) -> None:
    """
    Delete file after the associated object is deleted.
    """
    for field in instance._meta.get_fields():
        if isinstance(field, field_types):
            file_field = getattr(instance, field.name, None)
            if file_field and file_field.name:
                try:
                    default_storage.delete(file_field.name)
                    logger.info(f"Deleted file: {file_field.name}")
                except Exception as e:
                    logger.error(f"Error deleting file {file_field.name}: {e}")


def delete_file_after_object_update(
    instance: Model,
    field_types: Tuple[Type[FileField], ...] = (FileField, ImageField)) -> None:
    """
    Delete old files when a model instance's file fields are updated.
    """
    try:
        old_instance = instance.__class__.objects.get(pk=instance.pk)
    except ObjectDoesNotExist:
        logger.error("Previous instance not found.")
        return

    for field in instance._meta.get_fields():
        if isinstance(field, field_types):
            old_file_field = getattr(old_instance, field.name, None)
            new_file_field = getattr(instance, field.name, None)
            if old_file_field and old_file_field.name:
                if not new_file_field or old_file_field.name != new_file_field.name:
                    try:
                        default_storage.delete(old_file_field.name)
                        logger.info(f"Deleted old file: {old_file_field.name}")
                    except Exception as e:
                        logger.error(f"Error deleting old file {old_file_field.name}: {e}")