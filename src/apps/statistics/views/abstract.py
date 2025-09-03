from apps.base.views.generics import CustomGenericAPIView
from apps.statistics.utils.validate_date import validate_from_and_date_to_date


class AbstractStatisticsAPIView(CustomGenericAPIView):

    def get_queryset(self):
        from_date, to_date = validate_from_and_date_to_date(self.request)
        return self.queryset.filter(created_at__lte=to_date, created_at__gte=from_date)
