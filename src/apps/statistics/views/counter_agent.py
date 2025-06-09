from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta

from django.db.models import Prefetch
from django.utils.timezone import now


from rest_framework.response import Response

from apps.counter_agents.models import CounterAgent
from apps.orders.models import FoodOrder
from apps.statistics.views.abstract import AbstractStatisticsAPIView


class CounterAgentListAPIView(AbstractStatisticsAPIView):
    queryset = CounterAgent.objects.all().prefetch_related(
        Prefetch(
            "orders",
            queryset=FoodOrder.objects.select_related("food", "menu", "recipe"),
        )
    )

    def get(self, *args, **kwargs):
        counter_agents = self.get_queryset()

        data = []

        current_date = date(now().year, now().month, now().day)
        from_date = datetime.combine(current_date - relativedelta(months=1), time.min)
        to_date = datetime.combine(current_date, time.max)

        dates = {
            "from_date": from_date,
            "to_date": to_date
        }

        data.append(dates)

        for counter_agent in list(counter_agents):
            orders = counter_agent.orders.filter(status=True)
            if orders.exists():
                counter_data = {
                    "name": counter_agent.name,
                    "order_count": counter_agent.orders.count(),
                    "price": 0,
                }
                for order in orders:
                    counter_data["price"] += order.profit
                data.append(counter_data)
        data.sort(key=lambda x: x["price"], reverse=True)
        return Response(data)
