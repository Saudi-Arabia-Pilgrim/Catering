from django.urls import path
from apps.expenses.views import (
    MonthlySalaryUpdateAPIView,
    MonthlySalaryGenericAPIView,
    HiringExpenseCreateAPIView,
    HiringExpenseRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("monthly-salary/<int:id>/", MonthlySalaryGenericAPIView.as_view(), name="monthly_salary"),
    path("monthly-salary/update/<int:id>/", MonthlySalaryUpdateAPIView.as_view(), name="monthly_salary_update"),
    path("hiring-expense/", HiringExpenseCreateAPIView.as_view(), name="hiring_expense_create"),
    path("hiring-expense/<int:pk>/", HiringExpenseRetrieveUpdateDestroyAPIView.as_view(), name="hiring_expense_detail"),
]
