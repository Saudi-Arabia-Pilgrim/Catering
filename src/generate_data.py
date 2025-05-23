import logging
import os
import random
import string
from datetime import timedelta, datetime
from decimal import Decimal

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
from apps.expenses.models.hiring import HiringExpense
from apps.expenses.models.monthly_salary import MonthlySalary
from apps.foods.models.food import Food, FoodSection
from apps.foods.models.recipe_food import RecipeFood
from apps.menus.models.menu import Menu
from apps.menus.models.recipe import Recipe
from apps.products.models.product import Product
from apps.sections.models.measure import Measure
from apps.sections.models.section import Section
from apps.warehouses.models.warehouse import Warehouse
from apps.counter_agents.models.counter_agents import CounterAgent
from apps.guests.models import Guest
from apps.orders.models.food_order import FoodOrder
from apps.orders.models.hotel_order import HotelOrder
from apps.warehouses.models.experience import Experience
from apps.warehouses.models.products_used import ProductsUsed
from django.core.exceptions import ValidationError


def populate_data():
    # Clear existing data to avoid unique constraint violations
    try:
        # Delete in the correct order to avoid foreign key constraint violations
        print("Clearing existing data...")
        # First, clear data that depends on other models
        HotelOrder.objects.all().delete()  # Delete hotel orders first as they reference hotels, rooms, guests, and food orders
        FoodOrder.objects.all().delete()  # Delete food orders first as they reference Food, Menu, Recipe, and CounterAgent
        Guest.objects.all().delete()  # Delete guests before rooms as they reference rooms
        Order.objects.all().delete()  # Delete orders before transports
        Experience.objects.all().delete()  # Delete experiences before warehouses
        HiringExpense.objects.all().delete()  # Delete hiring expenses before users
        MonthlySalary.objects.all().delete()  # Delete monthly salaries before users
        CustomUser.objects.all().delete()  # Delete users

        # Delete models with dependencies
        Room.objects.all().delete()  # Now safe to delete rooms
        Recipe.objects.all().delete()  # Delete recipes before menus
        Menu.objects.all().delete()  # Delete menus before foods
        Food.objects.all().delete()  # Delete foods before recipe foods and food sections
        RecipeFood.objects.all().delete()  # Delete recipe foods
        FoodSection.objects.all().delete()  # Delete food sections
        ProductsUsed.objects.all().delete() # Delete products used
        Warehouse.objects.all().delete()  # Delete warehouses before products
        CounterAgent.objects.all().delete()  # Delete counter agents

        # Then clear the base models
        Transport.objects.all().delete()  # Delete transports
        Hotel.objects.all().delete()  # Delete hotels before room types
        RoomType.objects.all().delete()  # Delete room types
        Product.objects.all().delete()  # Delete products before sections and measures
        Section.objects.all().delete()  # Delete sections
        Measure.objects.all().delete()  # Delete measures
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
                            profit=50, gross_price=200)
        Room.objects.create(hotel=hotel1, room_type=double_room, capacity=2, count=15, occupied_count=0, net_price=250,
                            profit=75, gross_price=325)
        Room.objects.create(hotel=hotel2, room_type=suite_room, capacity=4, count=5, occupied_count=0, net_price=500,
                            profit=150, gross_price=650)

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
            start_year = max(2015, birthdate.year + 18)
            end_year = min(current_year, 2024)  # Updated to 2024
            # Ensure start_year is not greater than end_year
            if start_year > end_year:
                start_year = end_year
            date_come_year = random.randint(start_year, end_year)
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
        for _ in range(20):
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
            # Create 20 orders for each transport
            for _ in range(20):
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
                gross_fee = random.randint(400, 800)


                Order.objects.create(
                    transport=transport,
                    perform_date=perform_date,
                    from_location=from_loc,
                    to_location=to_loc,
                    status=Order.Status.CREATED,
                    passenger_count=str(passenger_count),
                    service_fee=service_fee,
                    gross_fee=gross_fee
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

    # Create Measures
    try:
        measures = [
            {"name": "Kilogram", "abbreviation": "kg"},
            {"name": "Gram", "abbreviation": "g"},
            {"name": "Liter", "abbreviation": "L"},
            {"name": "Milliliter", "abbreviation": "ml"},
            {"name": "Piece", "abbreviation": "pc"},
            {"name": "Box", "abbreviation": "box"},
            {"name": "Packet", "abbreviation": "pkt"},
            {"name": "Bottle", "abbreviation": "btl"},
            {"name": "Can", "abbreviation": "can"},
            {"name": "Dozen", "abbreviation": "dz"}
        ]

        for measure_data in measures:
            Measure.objects.create(
                name=measure_data["name"],
                abbreviation=measure_data["abbreviation"]
            )

        print("Measures created!")
    except ValidationError as e:
        print("Validation Error in Measures Creation:", e)
        return
    except Exception as e:
        print(f"Error in Measures Creation: {str(e)}")
        return

    # Verify measure data
    for measure in Measure.objects.all():
        print(f"Measure: {measure.name} | Abbreviation: {measure.abbreviation}")

    # Create Sections
    try:
        sections = [
            "Fruits",
            "Vegetables",
            "Meat",
            "Dairy",
            "Bakery",
            "Beverages",
            "Spices",
            "Grains",
            "Seafood",
            "Snacks",
            "Canned Goods",
            "Frozen Foods",
            "Condiments",
            "Breakfast",
            "Pasta",
            "Rice",
            "Oils",
            "Nuts",
            "Dried Fruits",
            "Organic",
            "Gluten-Free",
            "International"
        ]

        for section_name in sections:
            Section.objects.create(name=section_name)

        print("Sections created!")
    except ValidationError as e:
        print("Validation Error in Sections Creation:", e)
        return
    except Exception as e:
        print(f"Error in Sections Creation: {str(e)}")
        return

    # Verify section data
    for section in Section.objects.all():
        print(f"Section: {section.name}")

    # Create Food Sections
    try:
        # Sample food section names
        food_section_names = [
            "Suyuq", "Quyuq", "Xamirli", "Salatlar", "Ichimliklar",
            "Appetizers", "Main Courses", "Side Dishes", "Desserts", "Breakfast Items",
            "Lunch Specials", "Dinner Entrees", "Soups", "Salads", "Sandwiches",
            "Pasta Dishes", "Rice Dishes", "Seafood Specialties", "Vegetarian Options", "Vegan Choices",
            "Gluten-Free Selections", "Kids Menu", "Beverages", "Alcoholic Drinks"
        ]

        for section_name in food_section_names:
            FoodSection.objects.create(name=section_name)

        print("Food Sections created!")
    except ValidationError as e:
        print("Validation Error in Food Sections Creation:", e)
        return
    except Exception as e:
        print(f"Error in Food Sections Creation: {str(e)}")
        return

    # Create Products
    try:
        # Sample product data with appropriate measures
        product_data = [
            {"name": "Tomatoes", "measure": "kg"},
            {"name": "Potatoes", "measure": "kg"},
            {"name": "Onions", "measure": "kg"},
            {"name": "Carrots", "measure": "kg"},
            {"name": "Chicken", "measure": "kg"},
            {"name": "Beef", "measure": "kg"},
            {"name": "Rice", "measure": "kg"},
            {"name": "Pasta", "measure": "kg"},
            {"name": "Flour", "measure": "kg"},
            {"name": "Sugar", "measure": "kg"},
            {"name": "Salt", "measure": "g"},
            {"name": "Pepper", "measure": "g"},
            {"name": "Olive Oil", "measure": "L"},
            {"name": "Milk", "measure": "L"},
            {"name": "Cheese", "measure": "kg"},
            {"name": "Eggs", "measure": "dz"},
            {"name": "Bread", "measure": "pc"},
            {"name": "Apples", "measure": "kg"},
            {"name": "Oranges", "measure": "kg"},
            {"name": "Bananas", "measure": "kg"}
        ]

        # Get all measures and sections
        measures_dict = {m.abbreviation: m for m in Measure.objects.all()}
        sections = list(Section.objects.all())

        for product_info in product_data:
            # Get the appropriate measure for this product
            measure = measures_dict[product_info["measure"]]
            # Use the same measure for warehouse to ensure consistency
            measure_warehouse = measure
            section = random.choice(sections)

            # Set difference_measures to 1.0 for simplicity
            difference_measures = 1.0

            Product.objects.create(
                name=product_info['name'],
                measure=measure,
                measure_warehouse=measure_warehouse,
                difference_measures=difference_measures,
                section=section,
                status=random.choice([True, False])
            )

        print("Products created!")
    except ValidationError as e:
        print("Validation Error in Products Creation:", e)
        return
    except Exception as e:
        print(f"Error in Products Creation: {str(e)}")
        return

    # Verify product data
    for product in Product.objects.all():
        print(f"Product: {product.name} | Section: {product.section.name} | Status: {product.status}")

    # Create Warehouses
    try:
        # Get all products
        products = list(Product.objects.all())

        # Sample warehouse names
        warehouse_names = [
            "Main Storage", "Cold Storage", "Dry Goods", "Fresh Produce", 
            "Meat Storage", "Dairy Storage", "Bakery Storage", "Beverage Storage"
        ]

        # Create 30 warehouse entries with random products
        for i in range(30):
            product = random.choice(products)
            name = random.choice(warehouse_names) + f" {i+1}"
            gross_price = round(random.uniform(10.0, 1000.0), 2)
            arrived_count = round(random.uniform(100.0, 500.0), 2)
            count = arrived_count  # Set count equal to arrived_count to ensure full stock

            Warehouse.objects.create(
                product=product,
                status=True,
                gross_price=gross_price,
                count=count,
                arrived_count=arrived_count
            )

        print("Warehouses created!")
    except ValidationError as e:
        print("Validation Error in Warehouses Creation:", e)
        return
    except Exception as e:
        print(f"Error in Warehouses Creation: {str(e)}")
        return

    # Verify warehouse data
    for warehouse in Warehouse.objects.all()[:5]:  # Show just the first 5 to avoid too much output
        print(f"Warehouse: {warehouse.pk} | Product: {warehouse.product.name} | Count: {warehouse.count}/{warehouse.arrived_count}")

    # Create RecipeFood
    try:
        # Get all products
        products = list(Product.objects.all())

        # Create 30 recipe food entries with random products
        for i in range(30):
            product = random.choice(products)
            count = round(random.uniform(1.0, 10.0), 2)
            price = round(random.uniform(5.0, 100.0), 2)

            RecipeFood.objects.create(
                product=product,
                count=count,
                price=price,
                status=random.choice([True, False])
            )

        print("Recipe Foods created!")
    except ValidationError as e:
        print("Validation Error in Recipe Foods Creation:", e)
        return
    except Exception as e:
        print(f"Error in Recipe Foods Creation: {str(e)}")
        return

    # Verify recipe food data
    for recipe_food in RecipeFood.objects.all()[:5]:  # Show just the first 5 to avoid too much output
        print(f"Recipe Food: Product: {recipe_food.product.name} | Count: {recipe_food.count} | Price: {recipe_food.price}")

    # Create Foods
    try:
        # Sample food names
        food_names = [
            "Grilled Chicken", "Beef Stew", "Vegetable Soup", "Caesar Salad", 
            "Pasta Carbonara", "Margherita Pizza", "Chicken Curry", "Beef Burger", 
            "Fish and Chips", "Vegetable Stir Fry", "Mushroom Risotto", "Lamb Kebab",
            "Sushi Platter", "Pad Thai", "Butter Chicken", "Falafel Wrap",
            "Greek Salad", "Lasagna", "Shrimp Scampi", "Beef Tacos",
            "Chicken Alfredo", "Eggplant Parmesan", "Lobster Bisque", "Ramen Noodles"
        ]

        # Get all recipe foods and food sections
        recipe_foods = list(RecipeFood.objects.all())
        food_sections = list(FoodSection.objects.all())

        for food_name in food_names:
            # Create food
            food = Food.objects.create(
                name=food_name,
                section=random.choice(food_sections),
                status=True,
                net_price=0,  # Will be calculated based on recipes
                profit=Decimal(str(round(random.uniform(10.0, 50.0), 2))),
                gross_price=0  # Will be calculated based on recipes
            )

            # Add random recipe foods (between 2 and 5)
            num_recipes = random.randint(2, 5)
            selected_recipes = random.sample(recipe_foods, min(num_recipes, len(recipe_foods)))
            food.recipes.set(selected_recipes)

            # Calculate prices
            food.calculate_prices()
            food.save()

        print("Foods created!")
    except ValidationError as e:
        print("Validation Error in Foods Creation:", e)
        return
    except Exception as e:
        print(f"Error in Foods Creation: {str(e)}")
        return

    # Verify food data
    for food in Food.objects.all():
        print(f"Food: {food.name} | Net Price: {food.net_price} | Gross Price: {food.gross_price} | Recipes: {food.recipes.count()}")

    # Create Menus
    try:
        # Sample menu names
        menu_names = [
            "Breakfast Special", "Lunch Combo", "Dinner Deluxe", 
            "Weekend Brunch", "Holiday Feast", "Light Lunch", 
            "Executive Dinner", "Kids Menu", "Vegetarian Special",
            "Seafood Platter", "Steakhouse Special", "Italian Feast",
            "Asian Fusion", "Mediterranean Delight", "Mexican Fiesta",
            "Indian Thali", "Sushi Combo", "BBQ Platter", "Healthy Choice",
            "Dessert Sampler", "Tapas Selection", "Vegan Delight", "Gluten-Free Options"
        ]

        # Get all foods
        foods = list(Food.objects.all())

        for menu_name in menu_names:
            # Create menu
            menu = Menu.objects.create(
                name=menu_name,
                status=True,
                net_price=0,  # Will be calculated based on foods
                profit=Decimal(str(round(random.uniform(20.0, 100.0), 2))),
                gross_price=0  # Will be calculated based on foods
            )

            # Add random foods (between 3 and 6)
            num_foods = random.randint(3, 6)
            selected_foods = random.sample(foods, min(num_foods, len(foods)))
            menu.foods.set(selected_foods)

            # Calculate prices
            menu.calculate_prices()
            menu.save()

        print("Menus created!")
    except ValidationError as e:
        print("Validation Error in Menus Creation:", e)
        return
    except Exception as e:
        print(f"Error in Menus Creation: {str(e)}")
        return

    # Verify menu data
    for menu in Menu.objects.all():
        print(f"Menu: {menu.name} | Net Price: {menu.net_price} | Gross Price: {menu.gross_price} | Foods: {menu.foods.count()}")

    # Create Recipes
    try:
        # Sample recipe names
        recipe_names = [
            "Daily Special", "Weekly Plan", "Monthly Package", 
            "Corporate Event", "Wedding Catering", "Birthday Party",
            "Anniversary Dinner", "Graduation Celebration", "Holiday Gathering",
            "Business Lunch", "Family Reunion", "Cocktail Reception",
            "Charity Gala", "Product Launch", "Team Building Event",
            "Award Ceremony", "Retirement Party", "Baby Shower",
            "Engagement Party", "Bridal Shower", "Networking Event",
            "Conference Catering", "Sports Event", "Festival Food"
        ]

        # Get all menus
        menus = list(Menu.objects.all())

        for recipe_name in recipe_names:
            # Ensure we have at least 3 menus
            if len(menus) < 3:
                print("Not enough menus to create recipes")
                break

            # Randomly select 3 different menus for breakfast, lunch, and dinner
            selected_menus = random.sample(menus, 3)

            Recipe.objects.create(
                name=recipe_name,
                menu_breakfast=selected_menus[0],
                menu_lunch=selected_menus[1],
                menu_dinner=selected_menus[2],
                net_price=0,  # Will be calculated during save
                profit=Decimal(str(round(random.uniform(50.0, 200.0), 2))),
                gross_price=0  # Will be calculated during save
            )

        print("Recipes created!")
    except ValidationError as e:
        print("Validation Error in Recipes Creation:", e)
        return
    except Exception as e:
        print(f"Error in Recipes Creation: {str(e)}")
        return

    # Verify recipe data
    for recipe in Recipe.objects.all():
        print(f"Recipe: {recipe.name} | Net Price: {recipe.net_price} | Gross Price: {recipe.gross_price}")

    # Create HiringExpenses
    try:
        # Sample expense titles
        expense_titles = [
            "Visa Processing", "Flight Ticket", "Accommodation", "Transportation", 
            "Medical Check-up", "Work Permit", "Relocation Allowance", "Training", 
            "Equipment", "Uniform", "Documentation", "Recruitment Agency Fee"
        ]

        # Get all users
        users = list(CustomUser.objects.all())

        # Create hiring expenses for random users
        for _ in range(20):
            user = random.choice(users)
            title = random.choice(expense_titles)

            # Generate a random date in the past year
            days_ago = random.randint(1, 365)
            date = timezone.now() - timedelta(days=days_ago)

            # Generate a random cost between $100 and $5000
            cost = round(random.uniform(100.0, 5000.0), 2)

            HiringExpense.objects.create(
                user=user,
                title=title,
                date=date,
                cost=cost,
                status=random.choice([True, False])
            )

        print("Hiring Expenses created!")
    except ValidationError as e:
        print("Validation Error in Hiring Expenses Creation:", e)
        return
    except Exception as e:
        print(f"Error in Hiring Expenses Creation: {str(e)}")
        return

    # Verify hiring expense data
    for expense in HiringExpense.objects.all()[:5]:  # Show just the first 5 to avoid too much output
        print(f"Hiring Expense: {expense.title} | User: {expense.user.full_name} | Cost: ${expense.cost} | Paid: {expense.status}")

    # Create MonthlySalaries
    try:
        # Get all users
        users = list(CustomUser.objects.all())

        # Create monthly salaries for the past 20 months for random users
        for month in range(1, 21):
            # Generate a date for the first day of the month
            current_month = timezone.now().replace(day=1) - timedelta(days=30 * month)

            # Create salary records for random users
            for user in random.sample(users, min(10, len(users))):
                # Use the user's base_salary if available, otherwise generate a random one
                salary = user.base_salary if user.base_salary else round(random.uniform(2000.0, 10000.0), 2)

                MonthlySalary.objects.create(
                    user=user,
                    salary=salary,
                    date=current_month,
                    status=random.choice([True, False])
                )

        print("Monthly Salaries created!")
    except ValidationError as e:
        print("Validation Error in Monthly Salaries Creation:", e)
        return
    except Exception as e:
        print(f"Error in Monthly Salaries Creation: {str(e)}")
        return

    # Verify monthly salary data
    for salary in MonthlySalary.objects.all()[:5]:  # Show just the first 5 to avoid too much output
        print(f"Monthly Salary: {salary.user.full_name} | Month: {salary.month_year} | Amount: ${salary.salary} | Paid: {salary.status}")

    # Create CounterAgents
    try:
        # Sample counter agent data
        counter_agent_names = [
            "Royal Catering", "Elite Events", "Gourmet Solutions", "Deluxe Dining", 
            "Premium Provisions", "Luxury Feasts", "Corporate Cuisine", "Executive Eats",
            "Taste Masters", "Culinary Experts", "Fine Dining Co.", "Banquet Kings",
            "Catering Professionals", "Food Artisans", "Gala Catering", "Event Cuisine",
            "Flavor Fusion", "Dining Delights", "Celebration Foods", "Gourmet Express",
            "Feast Makers", "Culinary Creations", "Premier Catering", "Food Elegance"
        ]

        counter_agent_addresses = [
            "123 Main St, Riyadh, Saudi Arabia",
            "456 Business Ave, Jeddah, Saudi Arabia",
            "789 Corporate Blvd, Dammam, Saudi Arabia",
            "321 Commerce Way, Mecca, Saudi Arabia",
            "654 Industry Road, Medina, Saudi Arabia",
            "987 Enterprise Lane, Tabuk, Saudi Arabia",
            "147 Market Street, Abha, Saudi Arabia",
            "258 Trade Center, Taif, Saudi Arabia",
            "369 Culinary Blvd, Riyadh, Saudi Arabia",
            "741 Gourmet Ave, Jeddah, Saudi Arabia",
            "852 Flavor St, Dammam, Saudi Arabia",
            "963 Taste Lane, Mecca, Saudi Arabia",
            "159 Dining Road, Medina, Saudi Arabia",
            "357 Feast Blvd, Tabuk, Saudi Arabia",
            "486 Banquet St, Abha, Saudi Arabia",
            "792 Catering Ave, Taif, Saudi Arabia",
            "135 Event Lane, Riyadh, Saudi Arabia",
            "246 Food Court, Jeddah, Saudi Arabia",
            "579 Cuisine Blvd, Dammam, Saudi Arabia",
            "813 Delicacy St, Mecca, Saudi Arabia",
            "924 Culinary Lane, Medina, Saudi Arabia",
            "375 Gala Road, Tabuk, Saudi Arabia",
            "681 Premier Blvd, Abha, Saudi Arabia",
            "429 Elegance Ave, Taif, Saudi Arabia"
        ]

        for i in range(len(counter_agent_names)):
            counter_agent_type = random.choice([CounterAgent.Type.B2B, CounterAgent.Type.B2C])
            name = counter_agent_names[i]
            address = counter_agent_addresses[i]

            CounterAgent.objects.create(
                counter_agent_type=counter_agent_type,
                name=name,
                address=address,
                status=random.choice([True, False])
            )

        print("Counter Agents created!")
    except ValidationError as e:
        print("Validation Error in Counter Agents Creation:", e)
        return
    except Exception as e:
        print(f"Error in Counter Agents Creation: {str(e)}")
        return

    # Verify counter agent data
    for counter_agent in CounterAgent.objects.all():
        print(f"Counter Agent: {counter_agent.name} | Type: {counter_agent.counter_agent_type} | Status: {counter_agent.status}")

    # Create Guests
    try:
        # Sample guest data
        guest_names = [
            "Abdullah Al-Saud", "Mohammed Al-Qahtani", "Fatima Al-Ghamdi", "Aisha Al-Harbi", 
            "Omar Al-Shammari", "Khalid Al-Otaibi", "Layla Al-Zahrani", "Zainab Al-Dossari",
            "Yusuf Al-Qurashi", "Ibrahim Al-Harbi", "Noor Al-Mutairi", "Hassan Al-Zahrani",
            "Mariam Al-Qahtani", "Ali Al-Shammari", "Sara Al-Otaibi", "Ahmed Al-Saud",
            "Leila Al-Ghamdi", "Karim Al-Dossari", "Huda Al-Harbi", "Tariq Al-Mutairi",
            "Rania Al-Zahrani", "Jamal Al-Qurashi", "Samira Al-Shammari", "Faisal Al-Otaibi"
        ]

        # Get all hotels and rooms
        hotels = list(Hotel.objects.all())
        rooms = list(Room.objects.all())

        # Generate dates for check-in and check-out
        today = timezone.now().date()

        for i in range(len(guest_names)):
            # Select random hotel and room
            hotel = random.choice(hotels)
            room = random.choice([r for r in rooms if r.hotel == hotel])

            # Generate random check-in and check-out dates
            check_in = today + timedelta(days=random.randint(1, 30))
            check_out = check_in + timedelta(days=random.randint(1, 14))

            # Ensure count doesn't exceed room capacity
            count = random.randint(1, room.capacity)

            # Create guest
            guest = Guest(
                hotel=hotel,
                room=room,
                status=random.choice([Guest.Status.NEW, Guest.Status.COMPLETED, Guest.Status.CANCELED]),
                gender=random.choice([Guest.Gender.MALE, Guest.Gender.FEMALE]),
                full_name=guest_names[i],
                count=count,
                check_in=check_in,
                check_out=check_out
            )

            # The order_number is generated in the save method
            guest.save()

        print("Guests created!")
    except ValidationError as e:
        print("Validation Error in Guests Creation:", e)
        return
    except Exception as e:
        print(f"Error in Guests Creation: {str(e)}")
        return

    # Verify guest data
    for guest in Guest.objects.all():
        print(f"Guest: {guest.full_name} | Hotel: {guest.hotel.name} | Room: {guest.room.room_type.name} | Check-in: {guest.check_in} | Check-out: {guest.check_out}")

    # Create FoodOrders
    try:
        # ======== comment: helpers and imports ========
        from collections import defaultdict
        from django.db.models import Sum

        def get_available_stock(product):
            """
            ======== comment: returns current stock count for a given raw product ========
            """
            agg = (
                    Warehouse.objects
                    .filter(product=product, status=True)
                    .aggregate(total=Sum('count'))
                    or {}
            )
            return agg.get('total') or 0

        # ======== comment: preload foods and agents ========
        foods = list(Food.objects.prefetch_related('recipes__product'))
        counter_agents = list(CounterAgent.objects.filter(status=True))

        # ======== comment: sample delivery addresses ========
        addresses = [
            "123 Main St, Riyadh, Saudi Arabia",
            "456 Business Ave, Jeddah, Saudi Arabia",
            "789 Corporate Blvd, Dammam, Saudi Arabia",
            "321 Commerce Way, Mecca, Saudi Arabia",
            "654 Industry Road, Medina, Saudi Arabia",
            "987 Enterprise Lane, Tabuk, Saudi Arabia",
        ]

        # ======== comment: only seed orders for foods with sufficient raw-stock ========
        for _ in range(20):
            # ======== comment: pick a random dish ========
            food = random.choice(foods)

            # ======== comment: compute total ingredients needed ========
            products_needed = defaultdict(float)
            for rf in food.recipes.all():
                products_needed[rf.product] += float(rf.count) * 1  # quantity=1

            # ======== comment: skip if any ingredient is below requirement ========
            if any(get_available_stock(prod) < qty for prod, qty in products_needed.items()):
                continue

            # ======== comment: all ingredients available—create order ========
            counter_agent = random.choice(counter_agents)
            order_time    = timezone.now().date() + timedelta(days=random.randint(0, 30))
            address       = random.choice(addresses)

            FoodOrder.objects.create(
                food          = food,
                menu          = None,
                recipe        = None,
                counter_agent = counter_agent,
                order_time    = order_time,
                order_type    = FoodOrder.OrderType.ONCE,
                product_type  = FoodOrder.ProductType.FOOD,
                price         = food.gross_price,
                address       = address,
                product_count = 1,
                status        = random.choice([True, False]),
            )

        print("Food Orders created!")
    except ValidationError as e:
        print("Validation Error in Food Orders Creation:", e)
        return
    except Exception as e:
        print(f"Error in Food Orders Creation: {str(e)}")
        return

    # Verify food order data
    for food_order in FoodOrder.objects.all():
        product_info = ""
        if food_order.product_type == FoodOrder.ProductType.FOOD and food_order.food:
            product_info = f"Food: {food_order.food.name}"
        elif food_order.product_type == FoodOrder.ProductType.MENU and food_order.menu:
            product_info = f"Menu: {food_order.menu.name}"
        elif food_order.product_type == FoodOrder.ProductType.RECIPE and food_order.recipe:
            product_info = f"Recipe: {food_order.recipe.name}"

        print(
            f"Food Order: {food_order.food_order_id} | "
            f"{product_info} | "
            f"Counter Agent: {food_order.counter_agent.name} | "
            f"Price: {food_order.price} | "
            f"Count: {food_order.product_count}"
        )

    # Create HotelOrders
    try:
        # Get all hotels, rooms, guests, and food orders
        hotels = list(Hotel.objects.all())
        rooms = list(Room.objects.all())
        guests = list(Guest.objects.filter(status=Guest.Status.NEW))
        food_orders = list(FoodOrder.objects.filter(status=True))

        # Create hotel orders
        for _ in range(20):  # Create 20 hotel orders
            # Skip if no hotels, rooms, or guests available
            if not hotels or not rooms or not guests:
                continue

            # Select random hotel
            hotel = random.choice(hotels)

            # Select random room from the chosen hotel
            hotel_rooms = [r for r in rooms if r.hotel == hotel]
            if not hotel_rooms:
                continue
            room = random.choice(hotel_rooms)

            # Generate random check-in and check-out dates
            today = timezone.now()
            check_in = today + timedelta(days=random.randint(1, 30))
            check_out = check_in + timedelta(days=random.randint(1, 14))

            # Ensure count_of_people doesn't exceed room capacity
            count_of_people = random.randint(1, room.capacity)

            # Create hotel order
            hotel_order = HotelOrder.objects.create(
                hotel=hotel,
                room=room,
                order_status=random.choice([HotelOrder.OrderStatus.ACTIVE, HotelOrder.OrderStatus.COMPLETED]),
                food_service=random.choice([True, False]),
                check_in=check_in,
                check_out=check_out,
                count_of_people=count_of_people
            )

            # Add random guests to the hotel order
            available_guests = [g for g in guests if g.hotel == hotel and g.room == room]
            if available_guests:
                # Add up to 3 guests or all available guests, whichever is less
                selected_guests = random.sample(available_guests, min(3, len(available_guests)))
                hotel_order.guests.set(selected_guests)

            # Add random food orders to the hotel order if food_service is True
            if hotel_order.food_service and food_orders:
                # Add up to 3 food orders or all available food orders, whichever is less
                selected_food_orders = random.sample(food_orders, min(3, len(food_orders)))
                hotel_order.food_order.set(selected_food_orders)

        print("Hotel Orders created!")
    except ValidationError as e:
        print("Validation Error in Hotel Orders Creation:", e)
        return
    except Exception as e:
        print(f"Error in Hotel Orders Creation: {str(e)}")
        return

    # Verify hotel order data
    for hotel_order in HotelOrder.objects.all():
        print(f"Hotel Order: {hotel_order.order_id} | Hotel: {hotel_order.hotel.name} | Room: {hotel_order.room.room_type.name} | Check-in: {hotel_order.check_in} | Check-out: {hotel_order.check_out} | People: {hotel_order.count_of_people} | Food Service: {hotel_order.food_service}")

    # ======== comment: seed ProductsUsed entries ========
    try:
        # ======== comment: get all warehouses with available stock ========
        warehouses = list(Warehouse.objects.filter(status=True, count__gt=0))

        if not warehouses:
            print("No warehouses with available stock for ProductsUsed")
        else:
            # ======== comment: create 20 ProductsUsed entries ========
            for _ in range(20):
                # ======== comment: select random warehouse with available stock ========
                warehouse = random.choice(warehouses)

                # ======== comment: ensure we don't use more than available ========
                available = warehouse.count
                if available <= 0:
                    continue

                # ======== comment: generate random count and price ========
                used_count = str(round(random.uniform(0.1, min(5.0, available)), 2))
                price = round(random.uniform(10.0, 100.0) * float(used_count), 2)

                # ======== comment: create ProductsUsed entry ========
                ProductsUsed.objects.create(
                    warehouse=warehouse,
                    count=used_count,
                    price=price
                )

            print("ProductsUsed entries created!")
    except ValidationError as e:
        print("Validation Error in ProductsUsed Creation:", e)
        return
    except Exception as e:
        print(f"Error in ProductsUsed Creation: {str(e)}")
        return

    # ======== comment: verify ProductsUsed data ========
    for product_used in ProductsUsed.objects.all()[:5]:  # Show just the first 5 to avoid too much output
        print(f"ProductsUsed: Warehouse: {product_used.warehouse.pk} | Product: {product_used.warehouse.product.name} | Count: {product_used.count} | Price: {product_used.price}")

    # Create Experiences
    try:
        # Get all warehouses
        warehouses = list(Warehouse.objects.all())

        if not warehouses:
            print("No warehouses available to create experiences")
        else:
            # Create experiences for each warehouse
            for warehouse in warehouses[:20]:  # Limit to first 20 warehouses to avoid too many
                # Generate random count and price
                count = str(round(random.uniform(1.0, 20.0), 2))
                price = round(random.uniform(10.0, 500.0), 2)

                # Create experience
                Experience.objects.create(
                    warehouse=warehouse,
                    count=count,
                    price=price
                )

            print("Experiences created!")
    except ValidationError as e:
        print("Validation Error in Experiences Creation:", e)
        return
    except Exception as e:
        print(f"Erro    r in Experiences Creation: {str(e)}")
        return

    # Verify experience data
    for experience in Experience.objects.all():
        print(f"Experience: Warehouse: {experience.warehouse.pk} | Product: {experience.warehouse.product.name} | Count: {experience.count} | Price: {experience.price}")


if __name__ == "__main__":
    try:
        populate_data()
    except ValidationError as e:
        print("Validation Error:", e)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
