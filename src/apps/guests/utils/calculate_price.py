def calculate_guest_price(guest):
    from apps.guests.models import Guest

    days = (guest.check_out - guest.check_in).days
    if days < 1:
        days = 1

    overlapping_guests = Guest.objects.filter(
        room=guest.room,
        status=Guest.Status.COMPLETED,
        check_out__gt=guest.check_in,
        check_in__lt=guest.check_out
    ).exclude(pk=guest.pk).count() + 1

    guest.price = (guest.room.gross_price * days) / overlapping_guests