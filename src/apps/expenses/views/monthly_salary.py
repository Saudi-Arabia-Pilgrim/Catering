from django.http import Http404
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from dateutil.relativedelta import relativedelta
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.users.models import CustomUser
from apps.expenses.models import MonthlySalary
from apps.expenses.filters import MonthlySalaryFilter
from apps.expenses.serializers import MonthlySalarySerializer, MonthlySalaryCreateSerializer, MonthlySalaryUpdateSerializer
from apps.base.views import CustomGenericAPIView, CustomListAPIView


class MonthlySalaryListAPIView(CustomListAPIView):
    """
    Provides an API view to handle the list/filter/search of monthly salaries.

    This view is designed to fetch and return a list of monthly salaries,
    typically associated with a specific dataset or model. It extends
    the functionality of the `CustomListAPIView` to implement any custom
    behavior for management and retrieval of monthly salary-related data.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MonthlySalarySerializer
    queryset = MonthlySalary.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = MonthlySalaryFilter
    search_fields = ['user__email', 'user__full_name', 'month_year']

    def get_queryset(self):
        """
        Override get_queryset to filter by employee_id query parameter.
        """
        queryset = super().get_queryset()
        employee_id = self.request.query_params.get('employee_id')
        
        if employee_id:
            queryset = queryset.filter(user_id=employee_id)
        
        return queryset

class MonthlySalaryGenericAPIView(CustomGenericAPIView):
    """
    Handles API operations related to monthly salary data.

    Returns a list of monthly salaries for the authenticated employees.
    HR can use this endpoint to see a monthly breakdown and mark salaries as paid.
    """
    permission_classes = [IsAuthenticated]

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

    def post(self, request, *args, **kwargs):
        """
        Add monthly salary for an employee.
        Only HR, CEO, and ADMIN users can add salaries for employees.
        """
        # Check if the user has permission to add salaries
        if not (request.user.role in [CustomUser.UserRole.HR, CustomUser.UserRole.CEO, CustomUser.UserRole.ADMIN] or request.user.is_superuser):
            return Response(
                {"detail": "You do not have permission to add monthly salaries."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = MonthlySalaryCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                salary = serializer.save()
                response_serializer = MonthlySalarySerializer(salary)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"detail": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
