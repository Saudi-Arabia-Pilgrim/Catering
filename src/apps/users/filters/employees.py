import django_filters

from apps.users.models import CustomUser

class EmployeeFilter(django_filters.rest_framework.FilterSet):
    """
    order_number = django_filters.CharFilter(lookup_expr="icontains")
    from_location = django_filters.CharFilter(lookup_expr="icontains")
    to_location = django_filters.CharFilter(lookup_expr="icontains")
    status = django_filters.ChoiceFilter(choices=Order.Status.choices)
    perform_date = django_filters.DateFromToRangeFilter()
    service_fee = django_filters.RangeFilter()
    passenger_count = django_filters.NumberFilter()
    transport = django_filters.ModelChoiceFilter(queryset=Transport.objects.all())
    """
    email = django_filters.CharFilter(lookup_expr="icontains")
    full_name = django_filters.CharFilter(lookup_expr="icontains")
    phone_number = django_filters.CharFilter(lookup_expr="icontains")
    passport_number = django_filters.CharFilter(lookup_expr="icontains")

    role = django_filters.ChoiceFilter(choices=CustomUser.UserRole.choices)
    gender = django_filters.ChoiceFilter(choices=CustomUser.Gender.choices)

    base_salary = django_filters.NumericRangeFilter()

    class Meta:
        model = CustomUser
        fields = ["email", "full_name", "phone_number", "passport_number", "role", "gender", "base_salary"]



