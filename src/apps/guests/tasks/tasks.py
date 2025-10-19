from celery import shared_task
from django.db.models import Sum
from django.utils.timezone import now

from apps.rooms.models import Room
from apps.guests.models import Guest
from apps.orders.models import HotelOrder


@shared_task
def update_daily_guest_prices():
    today = now().date()

    # --- 1. HotelOrder statuslarini update qilish ---
    HotelOrder.objects.filter(check_out__lt=today).update(
        order_status=HotelOrder.OrderStatus.COMPLETED
    )
    HotelOrder.objects.filter(check_in__lte=today, check_out__gte=today).update(
        order_status=HotelOrder.OrderStatus.ACTIVE
    )
    HotelOrder.objects.filter(check_in__gt=today).update(
        order_status=HotelOrder.OrderStatus.PLANNED
    )

    # --- 2. Tugagan mehmonlarni update qilish ---
    finished_guests = Guest.objects.filter(
        check_out__lte=today,
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

    # --- 3. Yangi kun uchun mehmonlarga narx qo‘shish ---
    guests_today = Guest.objects.filter(
        status=Guest.Status.NEW,
        check_in__lte=today,
        check_out__gte=today
    ).select_related('room')

    updated_guest_count = 0

    for guest in guests_today:
        room = guest.room
        if not room:
            continue

        if room.capacity == 1:
            daily_price = room.gross_price
        else:
            same_room_guests = Guest.objects.filter(
                room=room,
                check_in__lte=today,
                check_out__gte=today,
                status=Guest.Status.NEW
            )
            guest_count = same_room_guests.aggregate(total=Sum("count"))["total"] or 1
            daily_price = round(room.gross_price / guest_count, 2) * guest.count

        guest.price += daily_price
        guest.save(update_fields=['price'])
        updated_guest_count += 1

    # --- 4. Room occupancy and status update (toliq refresh) ---
    for room in Room.objects.all():
        active_guests = Guest.objects.filter(
            room=room,
            status=Guest.Status.NEW,
            check_in__lte=today,
            check_out__gte=today
        )

        total_guests = active_guests.aggregate(total=Sum("count"))["total"] or 0

        room.occupied_count = total_guests
        room.remaining_capacity = max(room.capacity - total_guests, 0)
        room.is_busy = total_guests > 0
        room.save(update_fields=["is_busy", "occupied_count", "remaining_capacity"])

    return (
        f"{updated_guest_count} guests updated with prices, "
        f"{completed_guest_count} guests and {completed_order_count} hotel orders marked as completed."
    )
