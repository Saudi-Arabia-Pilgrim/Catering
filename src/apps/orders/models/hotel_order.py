import random
from math import ceil

from django.core.exceptions import ValidationError
from django.db import models, transaction

from apps.base.exceptions import CustomExceptionError
from apps.base.models import AbstractBaseModel
from apps.guests.utils.calculate_price import calculate_guest_price
from apps.orders.utils import new_id


class HotelOrderManager(models.Manager):
    def active_orders(self):
        return self.filter(order_status=HotelOrder.OrderStatus.ACTIVE)
    def completed_orders(self):
        return self.filter(order_status=HotelOrder.OrderStatus.COMPLETED)


class HotelOrder(AbstractBaseModel):
    class OrderStatus(models.TextChoices):
        ACTIVE = 'Active', 'Active'
        COMPLETED = 'Completed', 'Completed'

    objects = HotelOrderManager()

    hotel = models.ForeignKey(
        'hotels.Hotel',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        related_name="orders"
    )
    guests = models.ManyToManyField(
        "guests.Guest",
        related_name="hotel_orders",
        blank=True
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
    general_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if self.check_in >= self.check_out:
            raise ValidationError("Check-out sanasi check-in sanasidan keyin bo‘lishi kerak.")
        days = (self.check_out - self.check_in).days
        if days < 1:
            raise ValidationError("Mehmon kamida 1 kun qolishi kerak.")
        if self.count_of_people > self.room.capacity:
            raise ValidationError(f"Bu xonada faqat {self.room.capacity} kishi yashashi mumkin.")
        self.general_cost = self.room.gross_price * days

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            room = self.room

            needed_rooms = ceil(self.count_of_people / self.room.capacity)
            if room.available_count < needed_rooms:
                raise CustomExceptionError(code=400, detail="Here not enough empty rooms for this order.")

            with transaction.atomic():
                room.occupied_count += needed_rooms
                room.save(update_fields=["occupied_count"])
                self.full_clean()
                super().save(*args, **kwargs)

                for guest in self.guests.all():
                    calculate_guest_price(guest)
                    guest.save(update_fields=["price"])

        else:
            self.full_clean()
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        room = self.room
        needed_rooms = ceil(self.count_of_people / room.capacity)

        with transaction.atomic():
            room.occupied_count = max(room.occupied_count - needed_rooms, 0)
            room.save(update_fields=["occupied_count"])
            super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id}"
