import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import Http404

from apps.base.views import CustomGenericAPIView
from apps.expenses.serializers import MonthlySalarySerializer
from apps.expenses.models import MonthlySalary
from apps.users.models import CustomUser

class MonthlySalaryGenericAPIView(CustomGenericAPIView):
    """
    Handles API operations related to monthly salary data.

    Returns a list of monthly salaries for the authenticated employees.
    HR can use this endpoint to see a monthly breakdown and mark salaries as paid.
    """
    permission_classes = [IsAuthenticated]\

    def get(self, request, *args, **kwargs):
        """
        Returns a list of monthly salaries for the authenticated employees.
        HR, CEO, and admin users can specify an employee_id query parameter to view salaries for a specific employee.
        """
        # Check if employee_id query parameter is present
        employee_id = request.query_params.get('employee_id')

        if employee_id:
            # Check if the user has permission to view other employees' records
            if request.user.role in [CustomUser.UserRole.HR, CustomUser.UserRole.CEO, CustomUser.UserRole.ADMIN] or request.user.is_superuser:
                try:
                    # Get the employee with the specified ID
                    employee = get_object_or_404(CustomUser, id=employee_id)
                except Http404:
                    return Response(
                        {"detail": f"Employee with ID {employee_id} not found."},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                # If the user doesn't have permission, return a 403 Forbidden response
                return Response(
                    {"detail": "You do not have permission to view records for other employees."},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            # If no employee_id is specified, default to the authenticated user
            employee = request.user

        # Use employee.date_come if available, otherwise use the current date
        start_date = employee.date_come or timezone.now().date()
        start_date = start_date.replace(day=1)  # Set to the first day of the month
        end_date = timezone.now().date().replace(day=1)

        # Generate all month start dates between start_date and end_date
        months = []
        current = start_date
        while current < end_date:
            months.append(current)
            current += relativedelta(months=1)


        records = []
        for month in months:
            # Look for existing records for the same month and year
            record = MonthlySalary.objects.filter(
                user=employee,
                date__year=month.year,
                date__month=month.month
            ).first()
            if not record:
                # Optionally create a new record if it doesn't exist
                record = MonthlySalary.objects.create(
                    user=employee,
                    date=month,
                    salary=0.0,  # Default salary
                    status=False
                )
            records.append(record)
        serializer = MonthlySalarySerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
