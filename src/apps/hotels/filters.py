import django_filters
from apps.hotels.models import Hotel


class RoomWithGuestFilter(django_filters.FilterSet):
    room_type_name = django_filters.CharFilter(field_name="rooms__room_type__name", lookup_expr="icontains")

    class Meta:
        model = Hotel
        fields = ["room_type_name"]