from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP

from apps.guests.models import Guest
from apps.base.exceptions import CustomExceptionError


def calculate_prices_for_order(order):
    total_cost = Decimal("0.00")
    two_places = Decimal("0.01")

    if order.guest_type == order.GuestType.INDIVIDUAL and order.room and order.guests.exists():
        all_guests = list(order.guests.filter(status=Guest.Status.NEW))
        daily_price = order.room.gross_price
        guest_updates = []

        for guest in all_guests:
            guest_cost = Decimal("0.00")
            current_day = guest.check_in

            while current_day < guest.check_out:
                overlapping_guests = [g for g in all_guests if g.check_in <= current_day < g.check_out]
                guests_count = sum(g.count for g in overlapping_guests) or 1
                guest_cost += (daily_price / guests_count) * guest.count
                current_day += timedelta(days=1)

            guest.price = guest_cost.quantize(two_places, ROUND_HALF_UP)
            guest_updates.append(guest)
            total_cost += guest.price

        Guest.objects.bulk_update(guest_updates, ["price"])
        order.general_cost = total_cost.quantize(two_places)

    elif order.guest_type == order.GuestType.GROUP and order.rooms.exists() and order.guest_group_id:
        all_rooms = list(order.rooms.all())
        days = (order.check_out - order.check_in).days
        for room in all_rooms:
            total_cost += room.gross_price * days

        order.general_cost = total_cost.quantize(two_places)

    else:
        raise CustomExceptionError(code=400, detail="Guest type aniqlanmagan yoki noto‘g‘ri holat.")
