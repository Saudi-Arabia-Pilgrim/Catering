from django_filters import rest_framework as filters

from apps.hotels.models import Hotel
from apps.orders.models import HotelOrder
from apps.rooms.models import RoomType


class HotelFilterForGuests(filters.FilterSet):
    created_at_after = filters.DateFilter(field_name="created_at", lookup_expr="gte")
    created_at_before = filters.DateFilter(field_name="created_at", lookup_expr="lte")
    check_in_after = filters.DateFilter(field_name="check_in", lookup_expr="gte")
    check_in_before = filters.DateFilter(field_name="check_in", lookup_expr="lte")
    check_out_after = filters.DateFilter(field_name="check_out", lookup_expr="gte")
    check_out_before = filters.DateFilter(field_name="check_out", lookup_expr="lte")

    hotel = filters.ModelChoiceFilter(queryset=Hotel.objects.all())
    room_type = filters.ModelChoiceFilter(field_name="room__room_type", queryset=RoomType.objects.all())

    class Meta:
        model = HotelOrder
        fields = [
            "created_at_after", "created_at_before",
            "check_in_after", "check_in_before",
            "check_out_after", "check_out_before",
            "hotel", "room_type"
        ]