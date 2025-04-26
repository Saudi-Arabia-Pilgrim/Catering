from django.utils.timezone import now
from celery import shared_task
from apps.guests.models import Guest
from apps.orders.models import HotelOrder
from apps.rooms.models import Room


@shared_task
def update_daily_guest_prices():
    today = now().date()

    # 1. Faqat bugun xonada yashayotgan mehmonlarga narx qo‘shamiz
    guests_today = Guest.objects.filter(
        status=Guest.Status.NEW,
        check_in__lte=today,
        check_out__gt=today
    ).select_related('room')

    for guest in guests_today:
        room = guest.room
        if room.capacity == 1:
            daily_price = room.gross_price
        else:
            same_room_guests = Guest.objects.filter(
                room=room,
                check_in__lte=today,
                check_out__gt=today
            )
            guest_count = same_room_guests.count() or 1
            daily_price = round(room.gross_price / guest_count, 2)

        guest.price += daily_price
        guest.save(update_fields=['price'])

    # 2. Mehmonlik muddati tugaganlarni statusini COMPLETED ga o‘tkazamiz
    finished_guests = Guest.objects.filter(
        check_out__lte=today,
        status=Guest.Status.NEW
    ).prefetch_related('hotel_orders')

    completed_guest_count = 0
    completed_order_count = 0

    for guest in finished_guests:
        guest.status = Guest.Status.COMPLETED
        guest.save(update_fields=["status"])

        hotel_orders = guest.hotel_orders.all()
        completed_order_count += hotel_orders.update(order_status=HotelOrder.OrderStatus.COMPLETED)

        completed_guest_count += 1

    # 3. Har bir xonaning bandligini optimallashtirib yangilaymiz
    rooms = Room.objects.all()

    for room in rooms:
        guest_exists = Guest.objects.filter(
            room=room,
            status=Guest.Status.NEW,
            check_in__lte=today,
            check_out__gt=today
        ).exists()

        if room.is_busy != guest_exists:
            room.is_busy = guest_exists
            room.save(update_fields=['is_busy'])

    return f"{guests_today.count()} guest prices updated, {completed_guest_count} guests and {completed_order_count} hotel orders marked as completed."
