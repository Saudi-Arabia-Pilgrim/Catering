from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from apps.base.views import CustomListCreateAPIView, CustomRetrieveUpdateDestroyAPIView
from apps.sections.models import Measure
from apps.sections.serializers import MeasureSerializer


class MeasureRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer


class MeasureListCreateAPIView(CustomListCreateAPIView):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["status"]
    search_fields = ["name", "abbreviation"]
