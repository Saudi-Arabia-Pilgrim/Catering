from django.apps import apps
from django.db.models import Count, Sum, Max

Room = apps.get_model("rooms", "Room")


def get_grouped_room_data():
    grouped = (
        Room.objects
        .select_related("hotel", "room_type")
        .values(
            "hotel_id", "hotel__name",
            "room_type_id", "room_type__name"
        )
        .annotate(
            gross_price=Max("gross_price"),
            count=Count("id"),
            occupied_count=Sum("occupied_count"),
        )
    )

    # representative xonalarni bitta queryda olib kelamiz
    rooms = (
        Room.objects
        .select_related("hotel", "room_type")
        .order_by("hotel_id", "room_type_id", "id")
    )
    representative_map = {}
    for room in rooms:
        key = (str(room.hotel_id), str(room.room_type_id))
        if key not in representative_map:
            representative_map[key] = room

    # YAKUNIY LIST formatga o‘tkazamiz
    result = []

    for item in grouped:
        hotel_id = str(item["hotel_id"])
        room_type_id = str(item["room_type_id"])
        room_key = (hotel_id, room_type_id)

        rep_room = representative_map.get(room_key)

        count = item["count"] or 0
        occupied = item["occupied_count"] or 0
        capacity = getattr(rep_room, "capacity", 0)

        # remaining_capacity ni to'g'ri hisoblash uchun representative room dan olamiz
        # chunki u update_room_occupancy funksiyasi orqali to'g'ri hisoblanadi
        remaining_capacity = getattr(rep_room, "remaining_capacity", 0) if rep_room else 0
        
        result.append({
            "id": rep_room.id if rep_room else None,
            "hotel": item["hotel_id"],
            "hotel_name": item["hotel__name"],
            "room_type": item["room_type_id"],
            "room_name": item["room_type__name"],
            "floor": getattr(rep_room, "floor", None),
            "count": count,
            "occupied_count": occupied,
            "available_count": count - occupied,
            "remaining_capacity": remaining_capacity,  # Database dan to'g'ri qiymatni olamiz
            "capacity": capacity,
            "net_price": getattr(rep_room, "net_price", None),
            "profit": getattr(rep_room, "profit", None),
            "gross_price": item["gross_price"],
        })

    return result
