import random

from django.core.exceptions import ValidationError
from django.db import models

from apps.base.models import AbstractBaseModel


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
    guests = models.ManyToManyField("guests.Guest", related_name="hotel_orders", blank=True)
    order_status = models.CharField(choices=OrderStatus.choices)

    order_id = models.CharField(max_length=8, unique=True, editable=False)
    status = models.BooleanField(default=True)
    food_service = models.BooleanField(default=False)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    count_of_people = models.PositiveSmallIntegerField() # count_of_people xonani nechta kishi sig`ishidan kotta bo`lishi kerak emas.
    general_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        days = (self.check_out - self.check_in).days
        if days < 1:
            raise ValidationError("guest must live again 1 days.")

        self.general_cost = self.room.gross_price * days

        if self.count_of_people > self.room.capacity:
            raise ValidationError(f"This room can accommodate only {self.room.capacity} guest(s).")

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"№{random.randint(1000000, 9999999)}"

        if self.room.available_count < self.count_of_people:
            raise ValidationError("Not enough available rooms for this order.")

        self.room.occupied_count += self.count_of_people
        if self.room.occupied_count >= self.room.count:
            self.room.status = False
        self.room.save(update_fields=["occupied_count", "status"])

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.hotel.name
