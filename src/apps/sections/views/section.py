from apps.base.views import CustomListCreateAPIView, CustomRetrieveUpdateDestroyAPIView
from apps.sections.models import Section
from apps.sections.serializers import SectionSerializer


class SectionRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class SectionListCreateAPIView(CustomListCreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer