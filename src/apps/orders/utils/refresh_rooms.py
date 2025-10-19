import math
from django.db.models import Sum
from django.utils import timezone

from apps.base.exceptions import CustomExceptionError


def calculate_optimal_room_distribution(total_people, rooms_in_order, target_room):
    """
    Calculate optimal distribution of guests across rooms.
    This function distributes guests efficiently by filling smaller rooms first.
    
    Args:
        total_people: Total number of people to distribute
        rooms_in_order: List of room objects in the order
        target_room: The specific room we're calculating guests for
        
    Returns:
        Number of guests assigned to the target room
    """
    if not rooms_in_order or total_people <= 0:
        return 0
        
    print(f"📊 DIST: {total_people} odamni {len(rooms_in_order)} xonaga taqsimlaymiz")
    print(f"📊 DIST: Target room: {target_room.room_number} (ID: {target_room.id})")
    
    # Create a distribution plan
    distribution = {}
    remaining_people = total_people
    
    # Sort rooms by capacity (smaller rooms first for optimal filling)
    sorted_rooms = sorted(rooms_in_order, key=lambda r: (r.capacity or 0))
    
    # Distribute guests room by room, filling smaller rooms first
    for room in sorted_rooms:
        capacity = room.capacity or 0
        count = getattr(room, 'count', 1) or 1  # Safe way to get count, default to 1
        total_room_capacity = capacity * count
        
        print(f"📊 DIST: Room {room.room_number}: capacity={capacity}, count={count}, total_capacity={total_room_capacity}")
        
        if remaining_people <= 0 or total_room_capacity <= 0:
            distribution[room.id] = 0
            continue
            
        # Assign guests to this room type
        if remaining_people <= total_room_capacity:
            # All remaining people can fit in this room type
            distribution[room.id] = remaining_people
            remaining_people = 0
        else:
            # Fill this room type to capacity
            distribution[room.id] = total_room_capacity
            remaining_people -= total_room_capacity
            
        print(f"📊 DIST: Room {room.room_number} ga {distribution[room.id]} odam tayinlandi")
    
    result = distribution.get(target_room.id, 0)
    print(f"📊 DIST: Target room {target_room.room_number} uchun yakuniy natija: {result} odam")
    
    # Return the number of guests assigned to the target room
    return result

def update_room_occupancy(room, save=True):
    from apps.guests.models import Guest
    from apps.orders.models import HotelOrder

    now = timezone.now()

    if not room.capacity:
        raise CustomExceptionError(code=400, detail="Room capacity cannot be null or zero.")

    # Get room count safely, default to 1 if not set (treat as single physical room)
    room_count = getattr(room, 'count', 1) or 1

    print(f"🔍 DEBUG: Room {room.room_number} (ID: {room.id}) ni yangilamoqdamiz")
    print(f"🔍 DEBUG: capacity={room.capacity}, count={room_count}, total_capacity={room.capacity * room_count}")

    # === Individual guests ===
    # Get all active individual guests for this room (faqat hozirgi vaqtda xonada bo'lganlar)
    individual_guests_count = Guest.objects.filter(
        room=room,
        status=Guest.Status.NEW,
        check_in__lte=now,  # Check-in vaqti o'tgan
        check_out__gt=now   # Check-out vaqti hali kelmagan
    ).aggregate(total=Sum("count"))['total'] or 0

    print(f"🔍 DEBUG: Individual guests (hozir xonada): {individual_guests_count}")

    # === Group guests ===
    # Get all active group orders that include this room (faqat hozirgi vaqtda xonada bo'lganlar)
    group_orders = HotelOrder.objects.filter(
        rooms=room,
        order_status=HotelOrder.OrderStatus.ACTIVE,
        guest_type=HotelOrder.GuestType.GROUP,
        check_in__lte=now,  # Check-in vaqti o'tgan
        check_out__gt=now   # Check-out vaqti hali kelmagan
    ).select_related("guest_group").prefetch_related("rooms")

    print(f"🔍 DEBUG: {group_orders.count()} ta group order topildi (hozir xonada)")

    # Calculate group guests using optimal distribution algorithm
    group_guests_count = 0
    for order in group_orders:
        # Get actual number of people in this order
        people_in_order = (order.count_of_people or 0)
        if people_in_order <= 0 and order.guest_group:
            people_in_order = (order.guest_group.count or 0)
        if people_in_order <= 0:
            print(f"🔍 DEBUG: Order {order.id} - odamlar soni 0")
            continue
            
        rooms_in_order = list(order.rooms.all())
        if not rooms_in_order:
            print(f"🔍 DEBUG: Order {order.id} - xonalar yo'q")
            continue
            
        print(f"🔍 DEBUG: Order {order.id}: {people_in_order} odam, {len(rooms_in_order)} xona")
        
        # Calculate optimal distribution of guests across all rooms in this order
        guests_for_current_room = calculate_optimal_room_distribution(
            people_in_order, rooms_in_order, room
        )
        print(f"🔍 DEBUG: Room {room.room_number} ga {guests_for_current_room} odam tayinlandi")
        group_guests_count += guests_for_current_room

    # Calculate total guests for this room type
    total_guests_float = (individual_guests_count or 0) + group_guests_count
    # Use ceiling for occupancy calculation (can't have fractional guests)
    total_guests = math.ceil(total_guests_float)
    total_capacity = room.capacity * room_count

    print(f"🔍 DEBUG: individual={individual_guests_count}, group={group_guests_count}")
    print(f"🔍 DEBUG: total_guests={total_guests}, total_capacity={total_capacity}")

    # === Calculate occupancy ===
    if total_guests == 0:
        occupied_rooms = 0
        remaining_capacity = total_capacity
    else:
        # Calculate how many rooms are occupied or will be occupied
        occupied_rooms = math.ceil(total_guests / room.capacity) if room.capacity > 0 else 0
        remaining_capacity = max(total_capacity - total_guests, 0)

    print(f"🔍 DEBUG: occupied_rooms={occupied_rooms}, remaining_capacity={remaining_capacity}")

    room.occupied_count = min(occupied_rooms, room_count)
    room.available_count = max(room_count - room.occupied_count, 0)
    room.remaining_capacity = remaining_capacity
    room.is_busy = room.remaining_capacity == 0

    print(f"🔍 DEBUG: YAKUNIY: occupied_count={room.occupied_count}, remaining_capacity={room.remaining_capacity}, is_busy={room.is_busy}")

    if save:
        print(f"🔍 DEBUG: Room ni saqlayapmiz...")
        room.save(update_fields=[
            "occupied_count", "available_count", "remaining_capacity", "is_busy"
        ])
        print(f"🔍 DEBUG: Room saqlandi!")
