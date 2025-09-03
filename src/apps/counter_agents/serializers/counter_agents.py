from apps.base.serializers import CustomModelSerializer
from apps.counter_agents.models import CounterAgent


class CounterAgentSerializer(CustomModelSerializer):
    class Meta:
        model = CounterAgent
        fields = [
            "id",
            "counter_agent_type",
            "name",
            "address",
            "status",
            "created_at",
        ]
        read_only_fields = ["created_at"]
