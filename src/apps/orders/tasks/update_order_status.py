from celery import shared_task
from django.utils.timezone import now
from apps.orders.models import HotelOrder


@shared_task
def update_order_status_daily():
    today = now().date()

    orders = HotelOrder.objects.select_related("room").all()
    for order in orders:
        if today < order.check_in.date():
            new_status = HotelOrder.OrderStatus.PLANNED
        elif order.check_in.date() <= today <= order.check_out.date():
            new_status = HotelOrder.OrderStatus.ACTIVE
        else:
            new_status = HotelOrder.OrderStatus.COMPLETED

        if order.order_status != new_status:
            order.order_status = new_status
            order.save(update_fields=["order_status"])
