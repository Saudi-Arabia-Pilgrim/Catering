from apps.base.views import CustomUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404

from apps.expenses.serializers import MonthlySalarySerializer
from apps.expenses.models import MonthlySalary
from apps.users.models import CustomUser


class MonthlySalaryUpdateAPIView(CustomUpdateAPIView):
    """
    Endpoint to update the paid status of a monthly salary record.
    Expect a PATCH with a payload like {"status": true} to mark the salary as paid.
    HR, CEO, and admin users can specify an employee_id query parameter to update salaries for a specific employee.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MonthlySalarySerializer
    model = "MonthlySalary"
    lookup_field = "id"

    def get_object(self):
        """
        Override get_object to support employee_id query parameter.
        HR, CEO, and admin users can specify an employee_id query parameter to update salaries for a specific employee.
        """
        # Get the object ID from the URL
        obj_id = self.kwargs.get(self.lookup_field)

        # Check if employee_id query parameter is present
        employee_id = self.request.query_params.get('employee_id')

        if employee_id:
            # Check if the user has permission to update other employees' records
            if self.request.user.role in [CustomUser.UserRole.HR, CustomUser.UserRole.CEO, CustomUser.UserRole.ADMIN] or self.request.user.is_superuser:
                try:
                    # Get the employee with the specified ID
                    employee = get_object_or_404(CustomUser, id=employee_id)
                    # Get the monthly salary record for the specified employee
                    obj = get_object_or_404(MonthlySalary, id=obj_id, user=employee)
                    return obj
                except Http404:
                    raise Http404(f"Monthly salary record with ID {obj_id} not found for employee with ID {employee_id}.")
            else:
                # If the user doesn't have permission, return a 403 Forbidden response
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("You do not have permission to update records for other employees.")

        # If no employee_id is specified or the user doesn't have permission, use the default behavior
        # Get the monthly salary record for the authenticated user
        obj = get_object_or_404(MonthlySalary, id=obj_id, user=self.request.user)
        return obj

    def patch(self, request, *args, **kwargs):
        """
        Update the paid status of a monthly salary record.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
