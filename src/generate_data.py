import django
import os

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # Change to your actual settings module
django.setup()

from apps.rooms.models import RoomType, Room
from apps.hotels.models import Hotel
from django.core.exceptions import ValidationError


def populate_data():
    # Create Room Types
    single_room = RoomType.objects.create(name="Single Room", status=True)
    double_room = RoomType.objects.create(name="Double Room", status=False)
    suite_room = RoomType.objects.create(name="Fourth Room", status=True)

    print("Room types created!")

    # Create Hotels
    hotel1 = Hotel.objects.create(
        name="Luxury Inn",
        address="123 Luxury St, Riyadh, Saudi Arabia",
        email="contact@luxuryinn.com",
        phone_number="+9660111234567",
        rating=4.5,
    )

    hotel2 = Hotel.objects.create(
        name="Desert Oasis",
        address="456 Oasis Blvd, Jeddah, Saudi Arabia",
        email="info@desertoasis.com",
        phone_number="+9660117654321",
        rating=4.2,
    )

    print("Hotels created!")

    # Create Rooms
    Room.objects.create(hotel=hotel1, room_type=single_room, capacity=1, count=10, occupied_count=0, net_price=150,
                        profit=50)
    Room.objects.create(hotel=hotel1, room_type=double_room, capacity=2, count=15, occupied_count=0, net_price=250,
                        profit=75)
    Room.objects.create(hotel=hotel2, room_type=suite_room, capacity=4, count=5, occupied_count=0, net_price=500,
                        profit=150)

    print("Rooms created!")

    # Verify saved data
    for room in Room.objects.all():
        print(
            f"{room.hotel.name} - {room.room_type.name} | Available: {room.available_count} | Gross Price: {room.gross_price}")


if __name__ == "__main__":
    try:
        populate_data()
    except ValidationError as e:
        print("Validation Error:", e)
