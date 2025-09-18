from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from apps.orders.models.hotel_order import HotelOrder
from apps.orders.utils.calculate_price import calculate_prices_for_order


@receiver(post_save, sender=HotelOrder)
def hotel_order_post_save(sender, instance: HotelOrder, created, **kwargs):
    if instance is None:
        return

    # Avoid calculating on creation or when no guests are attached yet
    if created or not instance.guests.exists():
        return

    calculate_prices_for_order(instance)

    HotelOrder.objects.filter(pk=instance.pk).update(
        general_cost=instance.general_cost
    )


@receiver(m2m_changed, sender=HotelOrder.guests.through)
def hotel_order_guests_changed(sender, instance: HotelOrder, action, **kwargs):
    if action not in {"post_add", "post_remove", "post_clear"}:
        return

    if not instance.guests.exists():
        HotelOrder.objects.filter(pk=instance.pk).update(general_cost=0)
        return

    calculate_prices_for_order(instance)
    HotelOrder.objects.filter(pk=instance.pk).update(
        general_cost=instance.general_cost
    )
