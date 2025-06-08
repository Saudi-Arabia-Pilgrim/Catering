from django.db.models import Prefetch
from rest_framework.response import Response

from apps.counter_agents.models import CounterAgent
from apps.orders.models import FoodOrder
from apps.statistics.views.abstract import AbstractStatisticsAPIView


class CounterAgentListAPIView(AbstractStatisticsAPIView):
    queryset = CounterAgent.objects.prefetch_related(
        Prefetch(
            "orders",
            queryset=FoodOrder.objects.select_related("food", "menu", "recipe"),
        )
    )

    def get(self, *args, **kwargs):
        counter_agents = self.get_queryset()

        data = []

        for counter_agent in list(counter_agents):
            if counter_agent.orders.exists():
                counter_data = {
                    "name": counter_agent.name,
                    "order_count": counter_agent.orders.count(),
                    "price": 0,
                }
                for order in counter_agent.orders.all():
                    counter_data["price"] += order.profit
                data.append(counter_data)
        data.sort(key=lambda x: x["price"], reverse=True)
        return Response(data)
