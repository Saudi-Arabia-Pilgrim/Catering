from celery import shared_task

from django.utils.timezone import now

from apps.guests.models import Guest
from apps.rooms.models import Room


@shared_task
def update_guest_prices():
    today = now().date()

    rooms = Room.objects.all()

    for room in rooms:
        guests = Guest.objects.filter(
            room=room,
            status=Guest.Status.NEW,
            check_in__lte=today,
            check_out__gte=today
        )

        grouped = {}
        for guest in guests:
            key = (guest.check_in, guest.check_out)
            grouped.setdefault(key, []).append(guest)

        for (check_in, check_out), guest_group in grouped.items():
            total_people = sum(g.count for g in guest_group)
            if total_people == 0:
                continue

            price_per_person = room.gross_price / total_people

            for g in guest_group:
                g.price += round(price_per_person * g.count, 2)
                g.last_price_updated = today
                g.save(update_fields=["price", "last_price_updated"])
