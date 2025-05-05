from django.contrib.auth import get_user_model
from django.db import models
from apps.base.models import AbstractBaseModel
from django.conf import settings

class HiringExpense(AbstractBaseModel):
    """
    Model representing expenses for an employee hiring like visa, plain tickets, car payments and onboarding.

    User (ForeignKey)
    name (CharField)
    date (DateTimeField)
    cost (DecimalField)
    status (BooleanField)
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses',
        help_text="User who incurred the expense"
    )
    title = models.CharField(
        max_length=255,
        help_text="Name of the expense"
    )
    date = models.DateTimeField(
        help_text="Use a date when the expense was made!"
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Amount in USD"
    )
    status = models.BooleanField(
        default=False,
        help_text="Indicates whether the expense is paid or not."
    )

    def save(self, *args, **kwargs):
        user = get_user_model().objects.get(self.user_id)
        user.total_expenses + self.cost
        user.save()
        super.save(*args, **kwargs)



    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title}"




