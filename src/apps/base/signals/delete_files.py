from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save
from django.db.models import Model

from apps.base.services import (
    delete_file_after_object_deletion,
    delete_file_after_object_update
)



@receiver(post_delete)
def handle_file_deletion(sender, instance, **kwargs) -> None:
    """
    Delete associated files when a model instance is deleted.

    :param sender:
    :param instance:
    :param kwargs:
    :return: None
    """

    if isinstance(instance, Model):
        delete_file_after_object_deletion(instance)


@receiver(pre_save)
def handle_file_update(sender, instance, **kwargs) -> None:
    """
    Delete old files from storage when a model instance's file fields are updated.

    :param sender:
    :param instance:
    :param kwargs:
    :return: None
    """
    if isinstance(instance, Model) and instance.pk:
        existing_instance = sender.objects.filter(pk=instance.pk).first()
        if existing_instance:
            delete_file_after_object_update(instance)