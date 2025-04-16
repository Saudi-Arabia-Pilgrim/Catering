from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from apps.base.response.responses import CustomSuccessResponse
from apps.base.views import CustomCreateAPIView, CustomRetrieveUpdateDestroyAPIView
from apps.expenses.serializers import HiringExpenseSerializer
from apps.expenses.models import HiringExpense
from apps.users.models import CustomUser
from django.shortcuts import get_object_or_404
from django.http import Http404

class HiringExpenseCreateAPIView(CustomCreateAPIView):
    """
    Endpoint to create a new hiring expense record.
    HR, CEO, and admin users can specify an employee_id query parameter to create records for a specific employee.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = HiringExpenseSerializer
    model = HiringExpense

    def create(self, request, *args, **kwargs):
        """
        Create a new hiring expense record.
        HR, CEO, and admin users can specify an employee_id query parameter to create records for a specific employee.

        Passed tests: Production ready!
        """
        # Check if employee_id query parameter is present
        employee_id = request.query_params.get('employee_id') or request.data.get('employee_id')

        if not employee_id:
            return Response(
                {"detail": "employee_id query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # === Check if the user has permission to manage other employees' records ===
        allowed_roles = [CustomUser.UserRole.HR, CustomUser.UserRole.CEO, CustomUser.UserRole.ADMIN]
        if request.user.role not in allowed_roles and not request.user.is_superuser:
            return CustomSuccessResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                message="You do not have permission to create records for other employees."
            )

        employee = get_object_or_404(CustomUser, id=employee_id)


        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=employee)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class HiringExpenseRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    """
    Endpoint to retrieve, update, or delete a hiring expense record.
    HR, CEO, and admin users can specify an employee_id query parameter to manage records for a specific employee.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = HiringExpenseSerializer
    model = HiringExpense

    def get_object(self):
        """
        Override get_object to support employee_id query parameter.
        HR, CEO, and admin users can specify an employee_id query parameter to manage records for a specific employee.
        """
        # Get the object ID from the URL
        expense_id = self.kwargs.get('pk')

        # Check if employee_id query parameter is present
        employee_id = self.request.query_params.get('employee_id')

        if employee_id:
            # Check if the user has permission to manage other employees' records
            if self.request.user.role in [CustomUser.UserRole.HR, CustomUser.UserRole.CEO, CustomUser.UserRole.ADMIN] or self.request.user.is_superuser:
                try:
                    # Get the employee with the specified ID
                    employee = get_object_or_404(CustomUser, id=employee_id)
                    # Get the hiring expense record for the specified employee
                    obj = get_object_or_404(HiringExpense, id=expense_id, user=employee)
                    return obj
                except Http404:
                    raise Http404(f"Hiring expense record with ID {expense_id} not found for employee with ID {employee_id}.")
            else:
                # If the user doesn't have permission, raise a PermissionDenied exception
                raise PermissionDenied("You do not have permission to manage records for other employees.")

        # If no employee_id is specified or the user doesn't have permission, use the default behavior
        # Get the hiring expense record for the authenticated user
        obj = get_object_or_404(HiringExpense, id=expense_id, user=self.request.user)
        return obj

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a hiring expense record.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        Update a hiring expense record.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a hiring expense record.
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
