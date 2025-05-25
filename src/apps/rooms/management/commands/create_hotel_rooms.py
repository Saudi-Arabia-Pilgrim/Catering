from django.utils.text import slugify
from django.core.management.base import BaseCommand

from apps.hotels.models import Hotel
from apps.rooms.models import RoomType, Room

from decimal import Decimal


class Command(BaseCommand):
    help = "Create sample hotels, room types, and rooms."

    def handle(self, *args, **kwargs):
        # 1. Create 3 hotels
        hotels = []
        for i in range(1, 4):
            hotel, created = Hotel.objects.get_or_create(
                name=f"Hotel {i}",
                defaults={
                    "slug": slugify(f"Hotel {i}"),
                    "address": f"City Street {i}",
                    "email": f"hotel{i}@example.com",
                    "phone_number": f"+966011123456{i}",
                    "rating": Decimal("4.5")
                }
            )
            hotels.append(hotel)
            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Exists'}: {hotel.name}"))

        # 2. Create RoomTypes: 1-4 kishilik
        capacities = [1, 2, 3, 4]
        room_types = []

        for c in capacities:
            rt, created = RoomType.objects.get_or_create(
                name=f"{c} kishilik",
                defaults={"status": True}
            )
            room_types.append(rt)
            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Exists'}: RoomType {rt.name}"))

        # 3. Create 10 rooms for each hotel x room type
        for hotel in hotels:
            for room_type, cap in zip(room_types, capacities):
                for i in range(10):
                    room, created = Room.objects.get_or_create(
                        hotel=hotel,
                        room_type=room_type,
                        capacity=cap,
                        defaults={
                            "count": 10,
                            "remaining_capacity": cap,
                            "available_count": 1,
                            "occupied_count": 0,
                            "net_price": Decimal("100.00"),
                            "profit": Decimal("20.00"),
                            "gross_price": Decimal("120.00"),
                            "is_busy": False
                        }
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f"{'Created' if created else 'Exists'}: Room in {hotel.name} ({room_type.name})"
                    ))

        self.stdout.write(self.style.SUCCESS("✅ All sample data created successfully."))
