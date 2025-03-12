from django.db import models

from apps.base.models import AbstractBaseModel


class HotelOrderManager(models.Manager):
    def active_orders(self):
        return self.filter(order_status=HotelOrder.OrderStatus.ACTIVE)
    def completed_orders(self):
        return self.filter(order_status=HotelOrder.OrderStatus.COMPLETED)


class HotelOrder(AbstractBaseModel):
    class OrderStatus(models.IntegerChoices):
        ACTIVE = 1, 'Active'
        COMPLETED = 2, 'Completed'

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

    order_status = models.PositiveSmallIntegerField(choices=OrderStatus.choices)

    order_id = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    food_service = models.BooleanField(default=False)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    count_of_people = models.PositiveSmallIntegerField()
    general_cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.hotel.name