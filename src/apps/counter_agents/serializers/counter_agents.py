from apps.base.serializers import CustomModelSerializer
from apps.counter_agents.models import CounterAgent


class CounterAgentSerializer(CustomModelSerializer):
    class Meta:
        model = CounterAgent
        exclude = ["created_at", "created_by", "updated_at", "updated_by"]
        read_only_fields =["status"]

