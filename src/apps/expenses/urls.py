from django.urls import path
from apps.expenses.views import (
    MonthlySalaryListAPIView,
    MonthlySalaryUpdateAPIView,
    MonthlySalaryGenericAPIView,
    EmployeeHiringExpenseListCreateAPIView,
    EmployeeHiringExpenseRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("monthly-salary/list/", MonthlySalaryListAPIView.as_view(), name="monthly_salary_list"),
    path("monthly-salary/create/", MonthlySalaryGenericAPIView.as_view(), name="monthly_salary_create"),
    path("monthly-salary/<int:id>/", MonthlySalaryGenericAPIView.as_view(), name="monthly_salary_detail"),
    path("monthly-salary/update/<int:id>/", MonthlySalaryUpdateAPIView.as_view(), name="monthly_salary_update"),
  
    path('<uuid:employee_id>/expenses/', EmployeeHiringExpenseListCreateAPIView.as_view(),
         name='employee_hiring_expenses_list_create'),
    path("<uuid:employee_id>/expenses/<uuid:pk>/", EmployeeHiringExpenseRetrieveUpdateDestroyAPIView.as_view(),
         name="employee_hiring_expense_detail"),
]
