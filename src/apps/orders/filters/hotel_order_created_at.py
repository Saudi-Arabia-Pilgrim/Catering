from django_filters import rest_framework as filters

from apps.orders.models import HotelOrder


class HotelFilterInCreated(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()
    check_in = filters.DateFromToRangeFilter()
    check_out = filters.DateFromToRangeFilter()

    class Meta:
        model = HotelOrder
        fields = ["created_at", "check_in", "check_out"]