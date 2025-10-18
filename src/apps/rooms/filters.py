import django_filters

from apps.rooms.models import RoomType


class RoomTypeFilter(django_filters.FilterSet):
    """
    Filter for RoomType model based on its status field (True/False).
    """

    status = django_filters.BooleanFilter(
        field_name="status",
        label="Faollik holati (True=faol, False=noFaol)"
    )

    name = django_filters.Filter(field_name="name")

    class Meta:
        model = RoomType
        fields = ["name", "status"]
