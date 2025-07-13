from datetime import timedelta

from django.utils.timezone import now
from celery import shared_task
from apps.guests.models import Guest
from apps.orders.models import HotelOrder
from apps.rooms.models import Room


@shared_task
def update_daily_guest_prices():
    today = now().date()

    print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO WORKED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # 1. Bugungi kundan oldin chiqib ketgan mehmonlarni yakunlaymiz
    finished_guests = Guest.objects.filter(
        check_out__lte=today + timedelta(days=1),  # check_out <= today (ya'ni chiqib ketgan)
        status=Guest.Status.NEW
    ).prefetch_related('hotel_orders')

    completed_guest_count = 0
    completed_order_count = 0

    for guest in finished_guests:
        guest.status = Guest.Status.COMPLETED
        guest.room = None
        guest.save(update_fields=["status", "room", "room_name"])

        hotel_orders = guest.hotel_orders.all()
        completed_order_count += hotel_orders.update(order_status=HotelOrder.OrderStatus.COMPLETED)
        completed_guest_count += 1

        orders = guest.hotel_orders.all()
        for order in orders:
            order.order_status = HotelOrder.OrderStatus.COMPLETED
        HotelOrder.objects.bulk_update(orders, ["order_status"])

        room = getattr(guest, "room", None)
        if room:
            if room.capacity > room.guests.count():
                room.is_busy = False
                room.save()

    # 2. Hali yashab turgan mehmonlarga narx qo‘shamiz (shu kunda yashayotganlarga)
    guests_today = Guest.objects.filter(
        status=Guest.Status.NEW,
        check_in__lte=today,
        check_out__gte=today  # >= today, ya'ni bugun ham shu yerda
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

    # 3. Har bir xonaning bandligini yangilaymiz
    rooms = Room.objects.all()

    for room in rooms:
        guest_exists = Guest.objects.filter(
            room=room,
            status=Guest.Status.NEW,
            check_in__lte=today,
            check_out__gte=today
        ).exists()

        if room.is_busy != guest_exists:
            room.is_busy = guest_exists
            room.save(update_fields=['is_busy'])

    return f"{updated_guest_count} guests updated with prices, {completed_guest_count} guests and {completed_order_count} hotel orders marked as completed."
