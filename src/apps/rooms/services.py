from .models import Room


class RoomService:
    @staticmethod
    def delete_unoccupied_rooms(hotel, room_type):
        rooms = Room.objects.filter(
            hotel=hotel,
            room_type=room_type,
            is_busy=False
        )
        count = rooms.count()
        rooms.delete()
        return count


def update_rooms_price(rooms, validated_data):
    for room in rooms:
        for field in ["net_price", "profit"]:
            if field in validated_data:
                setattr(room, field, validated_data[field])
        room.apply_save_logic()

    Room.objects.bulk_update(
        rooms,
        ["net_price", "profit", "gross_price", "available_count", "occupied_count", "is_busy"]
    )


def create_additional_rooms(instance, validated_data, new_count, existing_count):
    diff = new_count - existing_count
    to_create = []

    for _ in range(diff):
        new_room = Room(
            hotel=instance.hotel,
            room_type=instance.room_type,
            net_price=validated_data.get("net_price", instance.net_price),
            profit=validated_data.get("profit", instance.profit),
            gross_price=validated_data.get("gross_price", instance.gross_price),
            capacity=instance.capacity,
            remaining_capacity=instance.capacity,
            available_count=1,
            occupied_count=0,
            is_busy=False,
            count=1,
        )
        new_room.apply_save_logic()
        to_create.append(new_room)

    Room.objects.bulk_create(to_create)


def delete_excess_rooms(rooms, new_count, existing_count):
    diff = existing_count - new_count
    to_delete = rooms.reverse()[:diff]
    for room in to_delete:
        room.delete()


