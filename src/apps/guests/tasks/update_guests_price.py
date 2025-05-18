from decimal import Decimal
from django.utils.timezone import now
from celery import shared_task
from apps.guests.models import Guest
from apps.orders.models import HotelOrder
from apps.rooms.models import Room


@shared_task
def update_daily_guest_prices():
    today = now().date()

    # 1. Tugagan mehmonlar (check_out <= bugun) statusini yangilaymiz
    completed_guests = Guest.objects.filter(
        status=Guest.Status.NEW,
        check_out__lt=today
    ).prefetch_related('hotel_orders')

    completed_guest_count = completed_order_count = 0
    for guest in completed_guests:
        guest.status = Guest.Status.COMPLETED
        guest.save(update_fields=["status"])
        completed_guest_count += 1

        orders_updated = guest.hotel_orders.update(order_status=HotelOrder.OrderStatus.COMPLETED)
        completed_order_count += orders_updated

    # 2. Hozir yashayotgan mehmonlarga narx qo‘shamiz
    staying_guests = Guest.objects.filter(
        status=Guest.Status.NEW,
        check_in__lte=today,
        check_out__gte=today
    ).select_related('room')

    updated_guest_count = 0

    for guest in staying_guests:
        room = guest.room
        capacity = room.capacity
        gross_price = room.gross_price or Decimal('0')

        # Shu xonada yashayotgan boshqa mehmonlarni topamiz
        roommates = Guest.objects.filter(
            room=room,
            status=Guest.Status.NEW,
            check_in__lte=today,
            check_out__gte=today
        )

        roommate_count = roommates.count()

        # 1 kishilik xonami yoki yolg'izmi? Narx to‘liq unga yoziladi
        if capacity == 1 or roommate_count == 1:
            daily_price = gross_price
        else:
            daily_price = (gross_price / roommate_count).quantize(Decimal('0.01'))

        guest.price += daily_price
        guest.last_price_updated = today
        guest.save(update_fields=["price", "last_price_updated"])
        updated_guest_count += 1

    # 3. Xonalarning bandlik holatini yangilaymiz
    rooms = Room.objects.all().select_related("room_type")
    for room in rooms:
        has_active_guests = Guest.objects.filter(
            room=room,
            status=Guest.Status.NEW,
            check_in__lte=today,
            check_out__gte=today
        ).exists()

        if room.is_busy != has_active_guests:
            room.is_busy = has_active_guests
            room.save(update_fields=["is_busy"])

    return (
        f"{updated_guest_count} guests updated with daily prices, "
        f"{completed_guest_count} guests marked as completed, "
        f"{completed_order_count} hotel orders marked as completed."
    )
