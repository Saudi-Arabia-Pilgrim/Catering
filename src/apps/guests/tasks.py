from django.utils.timezone import now
from celery import shared_task
from apps.guests.models import Guest
from apps.rooms.models import Room


@shared_task
def update_daily_guest_prices():
    today = now().date()

    # 1. Faqat bugun xonada yashayotgan mehmonlarga narx qo‘shamiz
    guests_today = Guest.objects.filter(
        check_in__lte=today,
        check_out__gt=today
    )

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
    )

    for guest in finished_guests:
        guest.status = Guest.Status.COMPLETED
        guest.save(update_fields=['status'])

    # 3. Har bir xonaning bandligini yangilaymiz
    for room in Room.objects.all():
        room.save()

    return f"{guests_today.count()} guest prices updated, {finished_guests.count()} guests marked as completed."
