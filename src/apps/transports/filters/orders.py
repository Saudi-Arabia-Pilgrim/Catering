import django_filters

from apps.transports.models import Order, Transport


class OrderFilter(django_filters.rest_framework.FilterSet):
    """
    Filter class for filtering ordered taxis!
    """
    order_number = django_filters.CharFilter(lookup_expr="icontains")
    from_location = django_filters.CharFilter(lookup_expr="icontains")
    to_location = django_filters.CharFilter(lookup_expr="icontains")
    status = django_filters.ChoiceFilter(choices=Order.Status.choices)
    perform_date = django_filters.DateFromToRangeFilter()
    service_fee = django_filters.RangeFilter()
    passenger_count = django_filters.NumberFilter()
    transport = django_filters.ModelChoiceFilter(queryset=Transport.objects.all())


    class Meta:
        model = Order
        fields = ["order_number", "from_location", "to_location", "status", "perform_date", "service_fee", "passenger_count", "transport"]
