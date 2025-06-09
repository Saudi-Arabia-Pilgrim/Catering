from django.db.models import Prefetch

from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.counter_agents.models import CounterAgent
from apps.orders.models import FoodOrder
from apps.statistics.utils.validate_date import validate_from_and_date_to_date


class CounterAgentListAPIView(CustomGenericAPIView):
    queryset = CounterAgent.objects.all().prefetch_related(
        Prefetch(
            "orders",
            queryset=FoodOrder.objects.select_related("food", "menu", "recipe"),
        )
    )

    def get(self, request, *args, **kwargs):
        counter_agents = self.get_queryset()
        from_date, to_date = validate_from_and_date_to_date(request)
        data = []

        data.append({"from_fate": from_date, "to_date": to_date})

        for counter_agent in list(counter_agents):
            orders = counter_agent.orders.filter(
                status=True, created_at__lte=to_date, created_at__gte=from_date
            )
            if orders.exists():
                counter_data = {
                    "name": counter_agent.name,
                    "order_count": counter_agent.orders.count(),
                    "price": 0,
                }
                for order in orders:
                    counter_data["price"] += order.profit
                data.append(counter_data)
        # data.sort(key=lambda x: x["price"], reverse=True)
        return Response(data)
