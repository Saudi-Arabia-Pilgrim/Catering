from apps.base.serializers import CustomModelSerializer
from apps.counter_agents.models import CounterAgent


class CounterAgentSerializer(CustomModelSerializer):
    class Meta:
        model = CounterAgent
        fields = [
            "id",
            "order_type",
            "name",
            "address",
            "status",
        ]
