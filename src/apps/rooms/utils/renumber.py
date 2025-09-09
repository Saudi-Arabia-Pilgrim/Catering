def renumber_rooms(rooms, new_floor=None):
    from apps.rooms.models import Room

    """
    Updates room_number and optionally floor, based on the new floor.
    """
    if not rooms:
        return

    floor = new_floor if new_floor is not None else rooms[0].floor

    for idx, room in enumerate(rooms):
        if new_floor is not None:
            room.floor = new_floor
        room.room_number = str(floor * 100 + idx)

    Room.objects.bulk_update(rooms, ["floor", "room_number"])
