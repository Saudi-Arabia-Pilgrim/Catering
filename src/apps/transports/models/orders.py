import random
import time

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.base.models import AbstractBaseModel
from apps.transports.models import Transport


class Order(AbstractBaseModel):
    """
    Order class for taxes.
    """

    class Status(models.TextChoices):
        """
        Status choices of the order.
        """
        CREATED = 'created', _('Created')
        CANCELED = 'canceled', _('Canceled')
        COMPLETED = 'completed', _('Completed')

    order_number = models.CharField(
        _("Order number"),
        max_length=10,
        unique=True,
    )
    transport = models.ForeignKey(
        Transport,
        on_delete=models.PROTECT,
        verbose_name=_("The Taxi Car")
    )
    perform_date = models.DateTimeField(
        _("Perform date"),
        help_text=_("The date and time the work needs to be performed"),
    )

    from_location = models.CharField(
        _("From location"),
        max_length=100,
        help_text=_("The pick-up location of the order")
    )
    to_location = models.CharField(
        _("To location"),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("The destination location of the order")
    )

    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED,
        help_text=_("The status of the order")
    )
    passenger_count = models.CharField(
        _("Passenger count"),
        max_length=10,
        blank=True,
        null=True,
        help_text=_("The number of passengers in the order")
    )
    service_fee = models.DecimalField(
        _("Taxi service fee"),
        max_digits=10,
        decimal_places=2,
        help_text=_("The service fee of the order")
    )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        constraints = [
            models.UniqueConstraint(
                fields=["order_number"],
                name="Order number already exists!"),
        ]

    @staticmethod
    def generate_order_number():
        timestamps = int(time.time()) % 1000000
        random_digits = random.randint(10, 99)
        order_number = f"{timestamps}{random_digits}"

        return order_number

    def clean(self):

        super().clean()

        if self.perform_date and self.perform_date < timezone.now():
            raise ValidationError(_("Perform Date cannot be in the past!"))

    def save(self, *args, **kwargs):
        if not self.order_number:
            order_number = self.generate_order_number()
            self.order_number = order_number
            super(Order, self).save(*args, **kwargs)
        super().save(*args, **kwargs)

