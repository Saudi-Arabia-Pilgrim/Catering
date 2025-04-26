import django_filters
from apps.expenses.models import HiringExpense
from django.db import models

class HiringExpenseFilter(django_filters.rest_framework.FilterSet):
    """
    Filter class for HiringExpense model.
    
    Provides filtering options for HiringExpense records.
    """
    # Filter by title with case-insensitive contains lookup
    title = django_filters.CharFilter(lookup_expr='icontains')
    
    # Filter by cost range
    cost = django_filters.RangeFilter()
    
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
        model = HiringExpense
        fields = ['title', 'cost', 'date', 'status', 'user', 'month', 'year']