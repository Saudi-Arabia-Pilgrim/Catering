import logging
import os
import random
from datetime import timedelta

import django
from django.utils import timezone

# Disable Django's logging to avoid permission issues
logging.disable(logging.CRITICAL)

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # Change to your actual settings module
django.setup()

from apps.rooms.models import RoomType, Room
from apps.hotels.models import Hotel
from apps.transports.models import Transport, Order
from django.core.exceptions import ValidationError


def populate_data():
    # Create Room Types
    single_room = RoomType.objects.create(name="Single Room", status=True)
    double_room = RoomType.objects.create(name="Double Room", status=True)
    suite_room = RoomType.objects.create(name="Suite", status=True)

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
    Room.objects.create(hotel=hotel1, room_type=single_room, capacity=1, count=10, occupied_count=2, net_price=150,
                        profit=50)
    Room.objects.create(hotel=hotel1, room_type=double_room, capacity=2, count=15, occupied_count=5, net_price=250,
                        profit=75)
    Room.objects.create(hotel=hotel2, room_type=suite_room, capacity=4, count=5, occupied_count=1, net_price=500,
                        profit=150)

    print("Rooms created!")

    # Verify saved data
    for room in Room.objects.all():
        print(
            f"{room.hotel.name} - {room.room_type.name} | Available: {room.available_count} | Gross Price: {room.gross_price}")

    # Create Transports
    transport1 = Transport.objects.create(
        name="Luxury Taxi",
        slug="luxury-taxi",
        name_of_driver="Ahmed Ali",
        address="789 Main St, Riyadh, Saudi Arabia",
        phone_number="+9660123456789",
        amount_of_people="4",
        status=True
    )

    transport2 = Transport.objects.create(
        name="Family Van",
        slug="family-van",
        name_of_driver="Mohammed Hassan",
        address="321 Side St, Jeddah, Saudi Arabia",
        phone_number="+9660987654321",
        amount_of_people="7",
        status=True
    )

    transport3 = Transport.objects.create(
        name="Executive Car",
        slug="executive-car",
        name_of_driver="Khalid Omar",
        address="456 Business Ave, Dammam, Saudi Arabia",
        phone_number="+9660555123456",
        amount_of_people="3",
        status=True
    )
    
    transport4 = Transport.objects.create(
        name="Malibu 2",
        slug="malibu-2",
        name_of_driver="Mohammed Hassan",
        address="321 Side St, Jeddah, Saudi Arabia",
        phone_number="+9660987654321",
        amount_of_people="7",
        status=True
    )

    print("Transports created!")

    # Create Orders
    # Generate future dates for orders
    now = timezone.now()
    future_dates = [now + timedelta(days=i) for i in range(1, 8)]

    # Sample locations
    pickup_locations = [
        "King Khalid International Airport, Riyadh",
        "Riyadh Park Mall",
        "Kingdom Centre, Riyadh",
        "Al Faisaliah Tower",
        "King Abdullah Financial District",
        "King Fahd International Airport, Dammam",
        "King Abdulaziz International Airport, Jeddah",
        "Prince Mohammad Bin Abdulaziz International Airport, Medina",
        "Al Rashid Mall, Al Khobar",
        "Mall of Arabia, Jeddah",
        "Al Noor Mall, Medina",
        "Al Othaim Mall, Al-Ahsa",
        "Haifa Mall, Jubail",
        "Al Qasr Mall, Riyadh",
        "Sahara Mall, Riyadh",
        "Red Sea Mall, Jeddah",
        "Stars Avenue Mall, Jeddah",
        "Al Andalus Mall, Jeddah",
        "Dhahran Mall, Dhahran",
        "Al Mousa Center, Al Hofuf"
    ]

    destination_locations = [
        "Diplomatic Quarter, Riyadh",
        "Granada Mall, Riyadh",
        "Tahlia Street, Riyadh",
        "Diriyah, Riyadh",
        "Al Bujairi Heritage Park",
        "Red Sea Mall, Jeddah",
        "Jeddah Corniche",
        "Al-Rashid Mall, Khobar",
        "King Fahd Causeway, Dammam",
        "Al-Ahsa National Park",
        "Prophet's Mosque, Medina",
        "Quba Mosque, Medina",
        "Al-Qassim Mall, Buraidah",
        "Abha Palace Hotel, Abha",
        "Taif Al-Hada Mountains"
    ]

    # Create orders for each transport
    transports = [transport1, transport2, transport3, transport4]

    for transport in transports:
        # Create 2 orders for each transport
        for _ in range(3):
            perform_date = random.choice(future_dates)
            from_loc = random.choice(pickup_locations)
            to_loc = random.choice(destination_locations)
            passenger_count = random.randint(1, int(transport.amount_of_people))
            service_fee = random.randint(50, 300)

            Order.objects.create(
                transport=transport,
                perform_date=perform_date,
                from_location=from_loc,
                to_location=to_loc,
                status=Order.Status.CREATED,
                passenger_count=str(passenger_count),
                service_fee=service_fee
            )

    print("Orders created!")

    # Verify transport data
    for transport in Transport.objects.all():
        print(f"Transport: {transport.name} | Driver: {transport.name_of_driver} | Capacity: {transport.amount_of_people}")

    # Verify order data
    for order in Order.objects.all():
        print(f"Order: {order.order_number} | Transport: {order.transport.name} | From: {order.from_location} | To: {order.to_location} | Fee: {order.service_fee}")


if __name__ == "__main__":
    try:
        populate_data()
    except ValidationError as e:
        print("Validation Error:", e)
