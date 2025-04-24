from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from apps.base.views import CustomListCreateAPIView, CustomRetrieveUpdateDestroyAPIView
from apps.counter_agents.models import CounterAgent
from apps.counter_agents.serializers import CounterAgentSerializer


class CounterAgentListCreateAPIView(CustomListCreateAPIView):
    serializer_class = CounterAgentSerializer
    queryset = CounterAgent.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["status", "order_type"]
    search_fields = ["name", "address"]


class CounterAgentRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    serializer_class = CounterAgentSerializer
    queryset = CounterAgent.objects.all()
