from django.db.models import Q

from django_filters import rest_framework as filters

from apps.orders.models.food_order import FoodOrder



class FoodOrderFilter(filters.FilterSet):

    is_active = filters.BooleanFilter(method="filter_is_active")

    class Meta:
        model = FoodOrder
        fields = ["product_type", "order_type", "counter_agent", "order_type", "order_time", "status"]

    def filter_is_active(self, queryset, name, value):
        if value is None:
            return queryset
        if value is True:
            return queryset.filter(status=FoodOrder.Status.PENDING)
        elif value is False:
            return queryset.filter(Q(status=FoodOrder.Status.ACCEPTED) | Q(status=FoodOrder.Status.CANCELED))
        return queryset