from django.conf import settings
from django.db import models

from apps.base.models import AbstractBaseModel


class MonthlySalary(AbstractBaseModel):
    """
    Model representing the monthly salary of an employee.

    employee (ForeignKey)
    salary (DecimalField)
    date (DateTimeField)
    status (BooleanField) -> Indicates whether the salary is paid for the current month or not.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='monthly_salaries'
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    date = models.DateTimeField(help_text="Use a date representing the first day of the month")
    status = models.BooleanField(
        default=False,
        help_text="Indicates whether the salary is paid for the current month or not."
    )

    class Meta:
        verbose_name = "Monthly Salary"
        verbose_name_plural = "Monthly Salaries"
        ordering = ["-created_at"]

    @property
    def month_year(self):
        return self.date.strftime("%B %Y")  # e.g., "March 2025"

    def __str__(self):
        return str(self.salary)
