from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.guests.models import GuestGroup, Guest
from apps.orders.models import HotelOrder
from apps.orders.utils.refresh_rooms import update_room_occupancy


@receiver(post_save, sender=HotelOrder)
def update_occupancy_on_order_save(sender, instance, **kwargs):
    if instance.guest_type == HotelOrder.GuestType.GROUP:
        for room in instance.rooms.all():
            update_room_occupancy(room)
    elif instance.guest_type == HotelOrder.GuestType.INDIVIDUAL and instance.room:
        update_room_occupancy(instance.room)


@receiver(post_save, sender=Guest)
def update_occupancy_on_guest_save(sender, instance, **kwargs):
    if instance.room:
        update_room_occupancy(instance.room)


@receiver(post_save, sender=GuestGroup)
def update_occupancy_on_guestgroup_save(sender, instance, **kwargs):
    orders = instance.orders.filter(guest_type=HotelOrder.GuestType.GROUP)
    for order in orders:
        for room in order.rooms.all():
            update_room_occupancy(room)
