import random

from apps.guests.models import Guest
from apps.guests.utils.calculate_price import calculate_guest_price

def prepare_bulk_guests(hotel, room, guests_data, check_in, check_out):
    guests = []

    for guest_data in guests_data:
        guest = Guest(
            hotel=hotel,
            room=room,
            full_name=guest_data["full_name"],
            gender=guest_data["gender"],
            check_in=check_in,
            check_out=check_out,
            room_name=room.room_type.name,
            order_number=f"№{random.randint(1000000, 9999999)}"
        )
        guest.full_clean()
        calculate_guest_price(guest)
        guests.append(guest)

    return guests
