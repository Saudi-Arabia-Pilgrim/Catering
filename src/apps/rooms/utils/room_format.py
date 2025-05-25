from django import apps
from django.db.models import Count, Sum

Room = apps.apps.get_model("rooms.Room")


def get_grouped_room_data(hotel=None):

    queryset = Room.objects.select_related("hotel", "room_type")

    if hotel:
        queryset = queryset.filter(hotel=hotel)

    queryset = (
        queryset
        .values(
            "room_type", "room_type__name",
            "hotel", "hotel__name", "gross_price"
        )
        .annotate(
            count=Count("id"),
            occupied_count=Sum("occupied_count"),
        )
    )

    result = []
    for item in queryset:
        count = item["count"] or 0
        occupied = item["occupied_count"] or 0

        rooms = Room.objects.filter(
            hotel_id=item["hotel"],
            room_type_id=item["room_type"]
        )

        remaining_capacity = Room.remaining_capacity_calculated(rooms)

        result.append({
            "hotel": item["hotel"],
            "hotel_name": item["hotel__name"],
            "room_type": item["room_type"],
            "room_name": item["room_type__name"],
            "count": count,
            "occupied_count": occupied,
            "available_count": count - occupied,
            "remaining_capacity": remaining_capacity,
            "gross_price": item["gross_price"],
        })

    return result