from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.guests.models import Guest
from apps.orders.utils.refresh_rooms import update_room_occupancy


# @receiver(post_save, sender=Guest)
# def update_room_occupancy_on_save(sender, instance, **kwargs):
#     if getattr(instance, "room", None):
#         update_room_occupancy(instance.room)
#
#
# @receiver(post_delete, sender=Guest)
# def update_room_occupancy_on_delete(sender, instance, **kwargs):
#     if getattr(instance, "room", None):
#         update_room_occupancy(instance.room)


@receiver([post_save, post_delete], sender=Guest)
def update_room_occupancy_signal(sender, instance, **kwargs):
    if getattr(instance, "room", None):
        update_room_occupancy(instance.room)
        instance.room.save(update_fields=[
            "occupied_count",
            "available_count",
            "remaining_capacity"
        ])
#
# @receiver(post_delete, sender=Guest)
# def update_room_occupancy_on_guest_delete(sender, instance, **kwargs):
#     if getattr(instance, "room", None):
#         update_room_occupancy(instance.room)


