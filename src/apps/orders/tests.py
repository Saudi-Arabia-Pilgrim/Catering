import pytest
from django.utils.timezone import now
from apps.guests.models import Guest
from apps.guests.tasks.tasks import update_daily_guest_prices


@pytest.mark.django_db
def test_update_daily_guest_prices():
    from apps.rooms.models import Room

    room = Room.objects.create(name="Test room", price=300)
    guest = Guest.objects.create(
        full_name="Test User",
        room=room,
        price=0,
        check_in=now().date(),
        check_out=now().date()
    )

    update_daily_guest_prices()

    guest.refresh_from_db()
    assert guest.price == 300
