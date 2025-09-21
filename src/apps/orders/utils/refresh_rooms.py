import math
from django.db.models import Sum
from django.utils import timezone

from apps.base.exceptions import CustomExceptionError

def update_room_occupancy(room, save=True):
    from apps.guests.models import Guest
    from apps.orders.models import HotelOrder

    now = timezone.now()

    if not room.capacity:
        raise CustomExceptionError(code=400, detail="Room capacity cannot be null or zero.")
    if not room.count:
        raise CustomExceptionError(code=400, detail="Room count cannot be null or zero.")

    # === Individual guests ===
    # Use timezone-aware datetime comparisons to include same-day times
    individual_guests_count = Guest.objects.filter(
        room=room,
        status=Guest.Status.NEW,
        check_in__lte=now,
        check_out__gte=now
    ).aggregate(total=Sum("count"))['total'] or 0

    # === Group guests ===
    group_orders = HotelOrder.objects.filter(
        rooms=room,
        check_in__lte=now,
        check_out__gte=now,
        order_status=HotelOrder.OrderStatus.ACTIVE,
        guest_type=HotelOrder.GuestType.GROUP
    ).select_related("guest_group").prefetch_related("rooms")

    # Расчёт: распределяем гостей группы пропорционально суммарной вместимости выбранных комнат
    group_guests_count = 0.0
    for order in group_orders:
        # Берём фактическое количество людей в ЭТОМ заказе: count_of_people
        # (если по какой-то причине его нет, используем размер всей группы)
        people_in_order = (order.count_of_people or 0)
        if people_in_order <= 0 and order.guest_group:
            people_in_order = (order.guest_group.count or 0)
        if people_in_order <= 0:
            continue
        rooms_in_order = list(order.rooms.all())
        # Общая вместимость всех выбранных типов комнат в заказе
        total_capacity_in_order = sum((r.capacity or 0) * (r.count or 0) for r in rooms_in_order)
        if total_capacity_in_order <= 0:
            continue
        # Доля текущего room в общей вместимости заказа
        room_capacity_total = (room.capacity or 0) * (room.count or 0)
        share = room_capacity_total / total_capacity_in_order
        # Количество гостей этой группы, приходящихся на данный тип комнаты
        group_guests_count += people_in_order * share

    # Считаем итоговое число гостей для данного типа комнаты
    total_guests_float = (individual_guests_count or 0) + group_guests_count
    # Для расчёта занятости и оставшейся вместимости берём потолок (нельзя заселить дробного гостя)
    total_guests = math.ceil(total_guests_float)
    total_capacity = room.capacity * room.count

    # === Bandlikni hisoblash ===
    if total_guests == 0:
        occupied_rooms = 0
        remaining_capacity = total_capacity
    else:
        # Nechta xona to'lgan yoki to'lishi mumkin bo'lganini hisoblaymiz
        occupied_rooms = math.ceil(total_guests / room.capacity) if room.capacity > 0 else 0
        remaining_capacity = max(total_capacity - total_guests, 0)

    room.occupied_count = min(occupied_rooms, room.count)
    room.available_count = max(room.count - room.occupied_count, 0)
    room.remaining_capacity = remaining_capacity
    room.is_busy = room.remaining_capacity == 0

    if save:
        room.save(update_fields=[
            "occupied_count", "available_count", "remaining_capacity", "is_busy"
        ])
