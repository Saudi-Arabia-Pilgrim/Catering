import django_filters
from apps.expenses.models import MonthlySalary
from django.db import models

class MonthlySalaryFilter(django_filters.rest_framework.FilterSet):
    """
    Filter class for MonthlySalary model.
    
    Provides filtering options for MonthlySalary records.
    """
    # Filter by salary range
    salary = django_filters.RangeFilter()
    
    # Filter by date range
    date = django_filters.DateFromToRangeFilter()
    
    # Filter by month and year separately
    month = django_filters.NumberFilter(field_name='date', lookup_expr='month')
    year = django_filters.NumberFilter(field_name='date', lookup_expr='year')
    
    # Filter by payment status
    status = django_filters.BooleanFilter()
    
    # Filter by user
    user = django_filters.NumberFilter(field_name='user__id')
    
    class Meta:
        model = MonthlySalary
        fields = ['salary', 'date', 'status', 'user', 'month', 'year']