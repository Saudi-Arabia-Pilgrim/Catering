from django.urls import path
from apps.expenses.views import (
    MonthlySalaryListAPIView,
    MonthlySalaryUpdateAPIView,
    MonthlySalaryGenericAPIView,
    HiringExpenseListAPIView,
    HiringExpenseCreateAPIView,
    HiringExpenseRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("monthly-salary/list/", MonthlySalaryListAPIView.as_view(), name="monthly_salary_list"),
    path("monthly-salary/create/", MonthlySalaryGenericAPIView.as_view(), name="monthly_salary_create"),
    path("monthly-salary/<int:id>/", MonthlySalaryGenericAPIView.as_view(), name="monthly_salary_detail"),
    path("monthly-salary/update/<int:id>/", MonthlySalaryUpdateAPIView.as_view(), name="monthly_salary_update"),
  
    path('hiring-expenses/list/', HiringExpenseListAPIView.as_view(), name='hiring_expenses_list'),
    path("hiring-expense/", HiringExpenseCreateAPIView.as_view(), name="hiring_expense_create"),
    path("hiring-expense/<uuid:pk>/", HiringExpenseRetrieveUpdateDestroyAPIView.as_view(), name="hiring_expense_detail"),
]
