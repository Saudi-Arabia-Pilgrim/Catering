"""
Celery tasks for room management
"""
from celery import shared_task
from django.utils import timezone
from apps.rooms.models import Room
from apps.guests.models import Guest
from apps.orders.models import HotelOrder
from apps.orders.utils.refresh_rooms import update_room_occupancy


@shared_task
def refresh_all_room_occupancy():
    """
    Barcha xonalarning occupancy holatini yangilaydi.
    Bu task har daqiqada ishga tushadi va check_out vaqti o'tgan mehmonlarni
    xonalardan chiqaradi.
    """
    now = timezone.now()
    print(f"🔄 TASK: Barcha xonalarni yangilash boshlandi - {now}")
    
    # 1. Check_out vaqti o'tgan mehmonlarning statusini COMPLETED ga o'zgartirish
    expired_guests = Guest.objects.filter(
        status=Guest.Status.NEW,
        check_out__lte=now  # Check-out vaqti o'tgan
    )
    
    expired_count = expired_guests.count()
    if expired_count > 0:
        print(f"🔄 TASK: {expired_count} ta mehmonning check_out vaqti o'tdi")
        expired_guests.update(status=Guest.Status.COMPLETED)
        print(f"✅ TASK: {expired_count} ta mehmon COMPLETED statusiga o'tkazildi")
    
    # 2. Check_out vaqti o'tgan orderlarning statusini COMPLETED ga o'zgartirish
    expired_orders = HotelOrder.objects.filter(
        order_status=HotelOrder.OrderStatus.ACTIVE,
        check_out__lte=now  # Check-out vaqti o'tgan
    )
    
    expired_orders_count = expired_orders.count()
    if expired_orders_count > 0:
        print(f"🔄 TASK: {expired_orders_count} ta orderning check_out vaqti o'tdi")
        expired_orders.update(order_status=HotelOrder.OrderStatus.COMPLETED)
        print(f"✅ TASK: {expired_orders_count} ta order COMPLETED statusiga o'tkazildi")
    
    # 2. Barcha xonalarni yangilash
    rooms = Room.objects.all()
    updated_count = 0
    
    for room in rooms:
        try:
            # Har bir xonaning occupancy holatini yangilash
            update_room_occupancy(room, save=True)
            updated_count += 1
        except Exception as e:
            print(f"❌ ERROR: Room {room.room_number} yangilanmadi: {str(e)}")
    
    print(f"✅ TASK: {updated_count} ta xona yangilandi")
    return f"Updated {expired_count} guests, {expired_orders_count} orders and {updated_count} rooms"


@shared_task
def refresh_specific_room_occupancy(room_id):
    """
    Bitta xonaning occupancy holatini yangilaydi.
    """
    try:
        room = Room.objects.get(id=room_id)
        update_room_occupancy(room, save=True)
        print(f"✅ TASK: Room {room.room_number} yangilandi")
        return f"Room {room.room_number} updated"
    except Room.DoesNotExist:
        print(f"❌ ERROR: Room {room_id} topilmadi")
        return f"Room {room_id} not found"
    except Exception as e:
        print(f"❌ ERROR: Room yangilanmadi: {str(e)}")
        return f"Error: {str(e)}"
