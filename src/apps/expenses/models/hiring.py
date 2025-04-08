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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.user.username}"




