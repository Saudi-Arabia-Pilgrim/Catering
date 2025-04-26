import logging
import os
import random
from datetime import timedelta, datetime
import string

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
from apps.users.models import CustomUser
from django.core.exceptions import ValidationError


def populate_data():
    # Clear existing data to avoid unique constraint violations
    try:
        # Delete in the correct order to avoid foreign key constraint violations
        print("Clearing existing data...")
        # First, clear data that depends on other models
        Order.objects.all().delete()
        Room.objects.all().delete()

        # Then clear the models they depend on
        Transport.objects.all().delete()
        Hotel.objects.all().delete()
        RoomType.objects.all().delete()

        # Clear users last as they might be referenced by other models
        # Note: This will also delete the superuser, so only uncomment if necessary
        # CustomUser.objects.filter(is_superuser=False).delete()
    except Exception as e:
        print(f"Error clearing existing data: {str(e)}")
        return

    try:
        # Create Room Types
        single_room = RoomType.objects.create(name="Single Room", status=True)
        double_room = RoomType.objects.create(name="Double Room", status=False)
        suite_room = RoomType.objects.create(name="Fourth Room", status=True)

        print("Room types created!")
    except ValidationError as e:
        print("Validation Error in Room Types:", e)
        return

    # Create Hotels
    try:
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
    except ValidationError as e:
        print("Validation Error in Hotels:", e)
        return

    # Create Rooms
    try:
        Room.objects.create(hotel=hotel1, room_type=single_room, capacity=1, count=10, occupied_count=0, net_price=150,
                            profit=50)
        Room.objects.create(hotel=hotel1, room_type=double_room, capacity=2, count=15, occupied_count=0, net_price=250,
                            profit=75)
        Room.objects.create(hotel=hotel2, room_type=suite_room, capacity=4, count=5, occupied_count=0, net_price=500,
                            profit=150)

        print("Rooms created!")
    except ValidationError as e:
        print("Validation Error in Rooms:", e)
        return

    # Verify saved data
    for room in Room.objects.all():
        print(
            f"{room.hotel.name} - {room.room_type.name} | Available: {room.available_count} | Gross Price: {room.gross_price}")

    # Create Users
    try:
        # Sample data for users
        first_names = ["Ahmed", "Mohammed", "Fatima", "Aisha", "Omar", "Khalid", "Layla", "Zainab", "Yusuf", "Ibrahim"]
        last_names = ["Al-Saud", "Al-Qahtani", "Al-Ghamdi", "Al-Harbi", "Al-Shammari", "Al-Otaibi", "Al-Zahrani", "Al-Dossari", "Al-Mutairi", "Al-Qurashi"]
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "company.sa"]
        countries = ["Saudi Arabia", "UAE", "Qatar", "Kuwait", "Bahrain", "Oman", "Egypt", "Jordan", "Lebanon", "Morocco"]

        # Track used emails to ensure uniqueness
        used_emails = set()

        # Create one user for each role
        for role in CustomUser.UserRole.choices:
            role_value = role[0]
            # Generate random user data
            full_name = f"{random.choice(first_names)} {random.choice(last_names)}"

            # Ensure email is unique
            email_base = full_name.lower().replace(' ', '.')
            domain = random.choice(domains)
            email = f"{email_base}@{domain}"

            # Add a random number if email is already used
            counter = 1
            while email in used_emails:
                email = f"{email_base}_{counter}@{domain}"
                counter += 1

            used_emails.add(email)

            gender = random.choice([CustomUser.Gender.MALE, CustomUser.Gender.FEMALE])[0]

            # Ensure valid birthdate (between 18 and 70 years old)
            current_year = datetime.now().year
            birthdate = datetime(random.randint(current_year - 70, current_year - 18), 
                                random.randint(1, 12), 
                                random.randint(1, 28)).date()

            # Ensure date_come is after birthdate and not in the future
            date_come_year = random.randint(max(2015, birthdate.year + 18), min(current_year, 2023))
            date_come = datetime(date_come_year, 
                                random.randint(1, 12), 
                                random.randint(1, 28)).date()

            from_come = random.choice(countries)

            # Generate random passport data
            passport_chars = string.ascii_uppercase + string.digits
            passport_number = ''.join(random.choice(passport_chars) for _ in range(9))
            given_by = f"Immigration Authority of {random.choice(countries)}"

            # Ensure validity_period is in the future
            validity_period = timezone.now() + timedelta(days=random.randint(365, 3650))

            # Generate random phone number with valid Saudi format
            phone_number = f"+966{random.randint(500000000, 599999999)}"

            # Generate random salary and expenses (positive values)
            base_salary = random.randint(3000, 15000)
            total_expenses = random.randint(1000, 5000)
            total_general_expenses = random.randint(500, 3000)

            # Create the user
            user = CustomUser.objects.create(
                full_name=full_name,
                email=email,
                gender=gender,
                birthdate=birthdate,
                date_come=date_come,
                from_come=from_come,
                passport_number=passport_number,
                given_by=given_by,
                validity_period=validity_period,
                phone_number=phone_number,
                role=role_value,
                base_salary=base_salary,
                total_expenses=total_expenses,
                total_general_expenses=total_general_expenses,
                is_staff=role_value in ['admin', 'ceo', 'hr', 'hotel', 'catering', 'transportation', 'analytics', 'warehouse'],
                is_active=True
            )

            # Set a password for the user
            user.set_password("password123")
            user.save()
    except ValidationError as e:
        print("Validation Error in User Creation (roles):", e)
        return
    except Exception as e:
        print(f"Error in User Creation (roles): {str(e)}")
        return

    # Create additional random users
    try:
        for _ in range(7):
            # Generate random user data
            full_name = f"{random.choice(first_names)} {random.choice(last_names)}"

            # Ensure email is unique
            email_base = full_name.lower().replace(' ', '.')
            domain = random.choice(domains)
            # Add a random suffix to reduce chance of collision
            email = f"{email_base}_{random.randint(1, 999)}@{domain}"

            # Check if email is already used
            counter = 1
            while email in used_emails:
                email = f"{email_base}_{random.randint(1000, 9999)}@{domain}"
                counter += 1

            used_emails.add(email)

            gender = random.choice([CustomUser.Gender.MALE, CustomUser.Gender.FEMALE])[0]
            role_value = random.choice(CustomUser.UserRole.choices)[0]

            # Create the user with minimal data
            user = CustomUser.objects.create(
                full_name=full_name,
                email=email,
                gender=gender,
                role=role_value,
                is_staff=role_value in ['admin', 'ceo', 'hr', 'hotel', 'catering', 'transportation', 'analytics', 'warehouse'],
                is_active=True
            )

            # Set a password for the user
            user.set_password("password123")
            user.save()
    except ValidationError as e:
        print("Validation Error in Additional User Creation:", e)
        return
    except Exception as e:
        print(f"Error in Additional User Creation: {str(e)}")
        return

    print("Users created!")

    # Verify user data
    for user in CustomUser.objects.all():
        print(f"User: {user.full_name} | Email: {user.email} | Role: {user.role}")

    # Create Transports
    try:
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
    except ValidationError as e:
        print("Validation Error in Transports Creation:", e)
        return
    except Exception as e:
        print(f"Error in Transports Creation: {str(e)}")
        return

    # Create Orders
    try:
        # Clear existing orders to avoid duplicate key errors
        Order.objects.all().delete()

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
            # Create 3 orders for each transport
            for _ in range(3):
                # Ensure from_location and to_location are different
                from_loc = random.choice(pickup_locations)
                to_loc = random.choice(destination_locations)
                while from_loc == to_loc:
                    to_loc = random.choice(destination_locations)

                perform_date = random.choice(future_dates)

                # Ensure passenger_count is valid for the transport
                max_passengers = int(transport.amount_of_people)
                passenger_count = random.randint(1, max_passengers)

                # Ensure service_fee is positive
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
    except ValidationError as e:
        print("Validation Error in Orders Creation:", e)
        return
    except Exception as e:
        print(f"Error in Orders Creation: {str(e)}")
        return

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
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
