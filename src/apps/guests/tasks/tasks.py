from datetime import timedelta
from django.utils.timezone import now
from celery import shared_task

from apps.guests.models import Guest
from apps.orders.models import HotelOrder
from apps.rooms.models import Room


@shared_task
def update_daily_guest_prices():
    today = now().date()

    HotelOrder.objects.filter(check_out__lt=today).update(
        order_status=HotelOrder.OrderStatus.COMPLETED
    )
    HotelOrder.objects.filter(check_in__lte=today, check_out__gte=today).update(
        order_status=HotelOrder.OrderStatus.ACTIVE
    )
    HotelOrder.objects.filter(check_in__gt=today).update(
        order_status=HotelOrder.OrderStatus.PLANNED
    )

    finished_guests = Guest.objects.filter(
        check_out__lte=today + timedelta(days=1),
        status=Guest.Status.NEW
    ).prefetch_related('hotel_orders')

    completed_guest_count = 0
    completed_order_count = 0

    for guest in finished_guests:
        guest.status = Guest.Status.COMPLETED
        guest.room = None
        guest.save(update_fields=["status", "room", "room_name"])

        orders = guest.hotel_orders.all()
        for order in orders:
            order.order_status = HotelOrder.OrderStatus.COMPLETED
        HotelOrder.objects.bulk_update(orders, ["order_status"])
        completed_order_count += len(orders)

        completed_guest_count += 1

    guests_today = Guest.objects.filter(
        status=Guest.Status.NEW,
        check_in__lte=today,
        check_out__gte=today
    ).select_related('room')

    updated_guest_count = 0

    for guest in guests_today:
        room = guest.room

        if room.capacity == 1:
            daily_price = room.gross_price
        else:
            same_room_guests = Guest.objects.filter(
                room=room,
                check_in__lte=today,
                check_out__gte=today,
                status=Guest.Status.NEW
            )
            guest_count = same_room_guests.count() or 1
            daily_price = round(room.gross_price / guest_count, 2)

        guest.price += daily_price
        guest.save(update_fields=['price'])

        updated_guest_count += 1

    for room in Room.objects.all():
        guest_exists = Guest.objects.filter(
            room=room,
            status=Guest.Status.NEW,
            check_in__lte=today,
            check_out__gte=today
        ).exists()

        if room.is_busy != guest_exists:
            room.is_busy = guest_exists
            room.save(update_fields=['is_busy'])

    return (
        f"{updated_guest_count} guests updated with prices, "
        f"{completed_guest_count} guests and {completed_order_count} hotel orders marked as completed."
    )
