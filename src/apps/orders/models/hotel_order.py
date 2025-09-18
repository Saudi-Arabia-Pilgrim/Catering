from django.db import models

from apps.orders.utils import new_id
from apps.base.models import AbstractBaseModel


class HotelOrderManager(models.Manager):
    def active_orders(self):
        return self.filter(order_status=HotelOrder.OrderStatus.ACTIVE)

    def completed_orders(self):
        return self.filter(order_status=HotelOrder.OrderStatus.COMPLETED)


class HotelOrder(AbstractBaseModel):
    class GuestType(models.TextChoices):
        INDIVIDUAL = "individual", "Individual"
        GROUP = "group", "Group"

    class OrderStatus(models.TextChoices):
        PLANNED = "Planned", "Planned"
        ACTIVE = 'Active', 'Active'
        COMPLETED = 'Completed', 'Completed'

    objects = HotelOrderManager()

    guest_type = models.CharField(
        max_length=20,
        choices=GuestType.choices,
        blank=True
    )

    hotel = models.ForeignKey(
        'hotels.Hotel',
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders'
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="orders"
    )
    rooms = models.ManyToManyField(
        "rooms.Room",
        blank=True,
        related_name="hotel_orders"
    )

    guest_group = models.ForeignKey(
        "guests.GuestGroup",
        models.PROTECT,
        blank=True,
        null=True
    )
    guests = models.ManyToManyField(
        "guests.Guest",
        related_name="hotel_orders",
        blank=True
    )

    food_order = models.ManyToManyField(
        "orders.FoodOrder",
        related_name="hotel_orders",
        blank=True,
    )

    order_status = models.CharField(
        choices=OrderStatus.choices,
        default=OrderStatus.ACTIVE,
        blank=True,
        null=True
    )

    order_id = models.CharField(default=new_id,
                                max_length=8,
                                unique=True,
                                editable=False
                                )
    food_service = models.BooleanField(default=False)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    count_of_people = models.PositiveSmallIntegerField()  # Bu xona sig‘imidan oshmasligi lozim.
    general_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)

    class Meta:
        ordering = ['-created_at']

    @property
    def profit(self):
        return self.room.profit

    # def clean(self):
    #     if self.check_in >= self.check_out:
    #         raise ValidationError("Check-out sanasi check-in sanasidan keyin bo‘lishi kerak.")
    #     days = (self.check_out - self.check_in).days
    #     if days < 1:
    #         raise ValidationError("Mehmon kamida 1 kun qolishi kerak.")
    #
    #     errors = {}
    #
    #     if self.guest_type == self.GuestType.INDIVIDUAL:
    #         if not self.room:
    #             errors["room"] = "Individual order uchun xona (room) ko‘rsatilishi shart."
    #         elif self.count_of_people > self.room.capacity:
    #             errors["room"] = f"Bu xonada faqat {self.room.capacity} kishi yashashi mumkin."
    #
    #     elif self.guest_type == self.GuestType.GROUP:
    #         if not self.guest_group:
    #             errors["__all__"] = "Group order uchun 'guest_group' kiritilishi shart."
    #         if not self.rooms.exists():
    #             errors["__all__"] = "Group order uchun hech bo‘lmaganda bitta xona kerak."
    #
    #     if errors:
    #         raise ValidationError(errors)
    #
    # def define_guest_type(self):
    #     if self.guest_group_id:
    #         self.guest_type = self.GuestType.GROUP
    #     elif self.guests.exists():
    #         self.guest_type = self.GuestType.INDIVIDUAL
    #     else:
    #         self.guest_type = ""
    #
    # def define_order_status(self):
    #     today = now().date()
    #     if self.check_in.date() > today:
    #         return self.OrderStatus.PLANNED
    #     elif self.check_out.date() < today:
    #         return self.OrderStatus.COMPLETED
    #     return self.OrderStatus.ACTIVE
    #
    # def save(self, *args, **kwargs):
    #     self.order_status = self.define_order_status()
    #     is_new = self._state.adding
    #
    #     if is_new:
    #         if self.guest_type == self.GuestType.INDIVIDUAL and self.room:
    #             needed_rooms = ceil(self.count_of_people / self.room.capacity)
    #             if self.room.available_count < needed_rooms:
    #                 raise CustomExceptionError(code=400, detail="Yetarli bo‘sh xona yo‘q.")
    #
    #             with transaction.atomic():
    #                 self.full_clean()
    #                 super().save(*args, **kwargs)
    #                 self.room.occupied_count += needed_rooms
    #                 self.room.save(update_fields=["occupied_count"])
    #
    #         elif self.guest_type == self.GuestType.GROUP:
    #             self.full_clean()
    #             super().save(*args, **kwargs)
    #
    #     else:
    #         self.full_clean()
    #         super().save(*args, **kwargs)
    #
    # def calculate_prices(self):
    #     total_cost = Decimal("0.00")
    #     two_places = Decimal("0.01")
    #
    #     if self.guest_type == self.GuestType.INDIVIDUAL and self.room and self.guests.exists():
    #         all_guests = list(self.guests.filter(status=Guest.Status.NEW))  # Prefilter
    #         daily_price = self.room.gross_price
    #         guest_updates = []
    #
    #         for guest in all_guests:
    #             guest_cost = Decimal("0.00")
    #             current_day = guest.check_in
    #
    #             while current_day < guest.check_out:
    #                 overlapping_guests = [
    #                     g for g in all_guests if g.check_in <= current_day < g.check_out
    #                 ]
    #                 guests_count = sum(g.count for g in overlapping_guests) or 1
    #                 guest_cost += (daily_price / guests_count) * guest.count
    #                 current_day += timedelta(days=1)
    #
    #             guest.price = guest_cost.quantize(two_places, rounding=ROUND_HALF_UP)
    #             guest_updates.append(guest)
    #             total_cost += guest.price
    #
    #         # ✅ bulk update
    #         Guest.objects.bulk_update(guest_updates, ["price"])
    #
    #         self.general_cost = total_cost.quantize(two_places, rounding=ROUND_HALF_UP)
    #
    #     elif self.guest_type == self.GuestType.GROUP and self.rooms.exists() and self.guest_group_id:
    #         all_rooms = list(self.rooms.all())  # BIR MARTA QUERY
    #         group_count = self.guest_group.count
    #         current_day = self.check_in
    #
    #         while current_day < self.check_out:
    #             for room in all_rooms:
    #                 room_price = room.gross_price
    #                 per_guest_price = room_price / room.capacity
    #                 total_cost += per_guest_price * room.capacity
    #             current_day += timedelta(days=1)
    #
    #         self.general_cost = total_cost.quantize(two_places, rounding=ROUND_HALF_UP)
    #
    #     else:
    #         raise CustomExceptionError(code=400, detail="Guest type aniqlanmagan yoki noto‘g‘ri holat.")
    #
    # def delete(self, *args, **kwargs):
    #     room = self.room
    #     needed_rooms = ceil(self.count_of_people / room.capacity)
    #
    #     with transaction.atomic():
    #         for guest in self.guests.all():
    #             guest.delete()
    #
    #         room.occupied_count = max(room.occupied_count - needed_rooms, 0)
    #         room.save(update_fields=["occupied_count"])
    #         super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id}"

