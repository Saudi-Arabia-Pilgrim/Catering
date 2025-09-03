import django_filters

from apps.transports.models import Transport


class TransportFilter(django_filters.rest_framework.FilterSet):
    """
    FilterSet for a Transport model that provides filtering capabilities for Transport objects.
    """
    name = django_filters.CharFilter(lookup_expr="icontains")
    name_of_driver = django_filters.CharFilter(lookup_expr="icontains")
    address = django_filters.CharFilter(lookup_expr="icontains")
    amount_of_people = django_filters.RangeFilter()
    status = django_filters.BooleanFilter()
    phone_number = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Transport
        fields = ["name", "name_of_driver", "address", "amount_of_people", "status", "phone_number"]
