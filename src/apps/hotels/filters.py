import django_filters
from apps.hotels.models import Hotel
from apps.rooms.models import RoomType


class RoomWithGuestFilter(django_filters.FilterSet):

    room_type = django_filters.ModelChoiceFilter(
        queryset=RoomType.objects.all(),
        field_name="room__room_type",
        to_field_name="name",
        label="Type of Room"
    )
    class Meta:
        model = Hotel
        fields = ["room_type"]