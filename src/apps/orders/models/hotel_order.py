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
    order_status = models.CharField(choices=OrderStatus.choices, blank=True, null=True)

    order_id = models.CharField(max_length=8, unique=True, editable=False)
    status = models.BooleanField(default=False)
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

        room = self.room

        self.general_cost = room.gross_price * days

        if self.count_of_people > room.capacity:
            raise ValidationError(f"This room can accommodate only {room.capacity} guest(s).")

    def save(self, *args, **kwargs):
        room = self.room

        if not self.order_id:
            self.order_id = f"№{random.randint(1000000, 9999999)}"

        if room.available_count < self.count_of_people:
            raise ValidationError("Not enough available rooms for this order.")

        room.occupied_count += self.count_of_people
        if room.occupied_count >= room.count:
            room.status = False
        room.save(update_fields=["occupied_count"])

        super().save(*args, **kwargs)

    def __str__(self):
        return self.hotel.name
