from django_filters import rest_framework as filters

from apps.orders.models.hotel_order import HotelOrder


class HotelOrderFilter(filters.FilterSet):
    room_type = filters.CharFilter(field_name="room__room_type__name", lookup_expr="icontains")

    class Meta:
        model = HotelOrder
        fields = ["room_type"]


