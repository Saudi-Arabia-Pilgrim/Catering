# def calculate_prices(self):
#     total_cost = Decimal("0.00")
#     two_places = Decimal("0.01")
#
#     # === Individual Guests bo‘lsa
#     if self.room and self.guests.exists():
#         daily_price = self.room.gross_price
#         for guest in self.guests.all():
#             guest_cost = Decimal("0.00")
#             current_day = guest.check_in
#
#             while current_day < guest.check_out:
#                 overlapping_guests = Guest.objects.filter(
#                     room=self.room,
#                     check_in__lte=current_day,
#                     check_out__gt=current_day,
#                     status=Guest.Status.NEW
#                 )
#
#                 guests_count = sum([g.count for g in overlapping_guests]) or 1
#                 guest_cost += (daily_price / guests_count) * guest.count
#                 current_day += timedelta(days=1)
#
#             guest_cost = guest_cost.quantize(two_places, rounding=ROUND_HALF_UP)
#             guest.price = guest_cost
#             guest.save(update_fields=["price"])
#             total_cost += guest_cost
#
#         self.general_cost = total_cost.quantize(two_places, rounding=ROUND_HALF_UP)
#
#     # === Guruhli Guests bo‘lsa
#     elif self.guest_group and self.rooms.exists():
#         group_count = self.guest_group.count
#         current_day = self.check_in
#
#         while current_day < self.check_out:
#             for room in self.rooms.all():
#                 room_price = room.gross_price
#                 per_guest_price = room_price / room.capacity
#                 total_cost += per_guest_price * room.capacity
#             current_day += timedelta(days=1)
#
#         self.general_cost = total_cost.quantize(two_places, rounding=ROUND_HALF_UP)

# def clean(self):
#     if self.check_in >= self.check_out:
#         raise ValidationError("Check-out sanasi check-in sanasidan keyin bo‘lishi kerak.")
#
#     days = (self.check_out - self.check_in).days
#     if days < 1:
#         raise ValidationError("Mehmon kamida 1 kun qolishi kerak.")
#
#     # === Individual mehmonlar uchun (guests + room)
#     if self.room and self.guests.exists():
#         if self.count_of_people > self.room.capacity:
#             raise ValidationError(f"Bu xonada faqat {self.room.capacity} kishi yashashi mumkin.")
#         self.general_cost = self.room.gross_price * days
#
#     # === Guruhli mehmonlar uchun (guest_group + rooms)
#     if self.guest_group and self.rooms.exists():
#         group_count = self.guest_group.count
#         total_capacity = sum(room.capacity for room in self.rooms.all())
#
#         if group_count > total_capacity:
#             raise ValidationError(f"Guruh sig‘imi {total_capacity} kishidan oshmasligi kerak.")
#
#         total_cost = Decimal("0.00")
#         current_day = self.check_in
#         while current_day < self.check_out:
#             for room in self.rooms.all():
#                 per_guest_price = room.gross_price / room.capacity
#                 total_cost += per_guest_price * min(room.capacity, group_count)
#             current_day += timedelta(days=1)
#
#         self.general_cost = total_cost.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)