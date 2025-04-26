from django.db.models import Prefetch
from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.counter_agents.models import CounterAgent
from apps.orders.models import FoodOrder


class CounterAgentListAPIView(CustomGenericAPIView):

    def get(self, *args, **kwargs):
        counter_agents = CounterAgent.objects.prefetch_related(
            Prefetch(
                "orders",
                queryset=FoodOrder.objects.select_related("food", "menu", "recipe"),
            )
        )

        data = []

        for counter_agent in counter_agents:
            if counter_agent.orders.exists():
                counter_datas = {
                    "name": counter_agent.name,
                    "order_count": counter_agent.orders.count(),
                    "price": 0
                }
                for order in counter_agent.orders.all():
                    counter_datas["price"] += order.profit
                data.append(counter_datas)
        data.sort(key=lambda x: x["price"], reverse=True)
        return Response(data)