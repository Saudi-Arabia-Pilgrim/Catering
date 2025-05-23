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
            "id", "room_type", "room_type__name",
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
        result.append({
            "id": item["id"],
            "hotel": item["hotel"],
            "hotel_name": item["hotel__name"],
            "room_type": item["room_type"],
            "room_name": item["room_type__name"],
            "count": count,
            "occupied_count": occupied,
            "available_count": count - occupied,
            "gross_price": item["gross_price"],
        })

    return result



# def get_grouped_room_data(hotel=None):
#     room_filter = Q()
#     if hotel:
#         room_filter &= Q(hotel=hotel)
#
#     # Prefetch only relevant rooms (optionally filtered by hotel)
#     rooms_qs = Room.objects.filter(room_filter).select_related("hotel")
#     room_types = RoomType.objects.prefetch_related(
#         Prefetch("rooms", queryset=rooms_qs, to_attr="prefetched_rooms")
#     )
#
#     data = []
#
#     for item in room_types:
#         rooms = item.prefetched_rooms
#
#         if not rooms:
#             continue  # Skip empty room sets
#
#         occupied_count = sum(1 for r in rooms if r.is_busy)
#         available_count = len(rooms) - occupied_count
#         first_room = rooms[0]
#
#         data.append({
#             "room_type": item.id,
#             "room_name": item.name,
#             "hotel": first_room.hotel_id,
#             "hotel_name": first_room.hotel.name,
#             "gross_price": first_room.gross_price,
#             "occupied_count": occupied_count,
#             "available_count": available_count,
#             "count": len(rooms)
#         })
#
#     return data

