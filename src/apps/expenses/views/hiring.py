from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.users.models import CustomUser
from apps.expenses.models import HiringExpense
from apps.expenses.filters import HiringExpenseFilter
from apps.expenses.serializers import HiringExpenseSerializer
from apps.base.response.responses import CustomSuccessResponse
from apps.base.views import CustomCreateAPIView, CustomRetrieveUpdateDestroyAPIView, CustomListAPIView


class EmployeeHiringExpenseListCreateAPIView(CustomListAPIView, CustomCreateAPIView):
    """
    List all hiring expenses for a specific employee or create a new one.
    Endpoint: GET/POST /api/v1/employee/{employee_id}/expenses/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = HiringExpenseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = HiringExpenseFilter
    search_fields = ['title', 'user__email', 'user__full_name']

    def get_queryset(self):
        employee_id = self.kwargs.get('employee_id')
        employee = get_object_or_404(CustomUser, id=employee_id)
        
        # Check permissions
        allowed_roles = [CustomUser.UserRole.HR, CustomUser.UserRole.CEO, CustomUser.UserRole.ADMIN]
        if (self.request.user.id != employee.id and 
            self.request.user.role not in allowed_roles and 
            not self.request.user.is_superuser):
            raise PermissionDenied("You do not have permission to view this employee's expenses.")
        
        return HiringExpense.objects.filter(user=employee)

    def create(self, request, *args, **kwargs):
        employee_id = self.kwargs.get('employee_id')
        employee = get_object_or_404(CustomUser, id=employee_id)
        
        # Check permissions
        allowed_roles = [CustomUser.UserRole.HR, CustomUser.UserRole.CEO, CustomUser.UserRole.ADMIN]
        if (self.request.user.id != employee.id and 
            self.request.user.role not in allowed_roles and 
            not self.request.user.is_superuser):
            raise PermissionDenied("You do not have permission to create expenses for this employee.")
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=employee)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmployeeHiringExpenseRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific hiring expense for an employee.
    Endpoint: GET/PATCH/DELETE /api/v1/employee/{employee_id}/expenses/{uuid:pk}/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = HiringExpenseSerializer

    def get_object(self):
        employee_id = self.kwargs.get('employee_id')
        expense_id = self.kwargs.get('pk')
        
        employee = get_object_or_404(CustomUser, id=employee_id)
        
        # Check permissions
        allowed_roles = [CustomUser.UserRole.HR, CustomUser.UserRole.CEO, CustomUser.UserRole.ADMIN]
        if (self.request.user.id != employee.id and 
            self.request.user.role not in allowed_roles and 
            not self.request.user.is_superuser):
            raise PermissionDenied("You do not have permission to access this employee's expenses.")
        
        return get_object_or_404(HiringExpense, id=expense_id, user=employee)
