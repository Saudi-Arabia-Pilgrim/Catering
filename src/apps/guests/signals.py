from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.guests.models import Guest


@receiver(post_save, sender=Guest)
def update_room_occupancy_on_save(sender, instance, **kwargs):
    instance.room.refresh_occupancy()


@receiver(post_delete, sender=Guest)
def update_room_occupancy_on_delete(sender, instance, **kwargs):
    instance.room.refresh_occupancy()


@receiver([post_save, post_delete], sender=Guest)
def update_room_occupancy(sender, instance, **kwargs):
    if instance.room:
        instance.room.refresh_occupancy()
        instance.room.save(update_fields=[
            "occupied_count",
            "available_count",
            "remaining_capacity"
        ])

@receiver(post_delete, sender=Guest)
def update_room_occupancy_on_guest_delete(sender, instance, **kwargs):
    if instance.room:
        instance.room.refresh_occupancy()


