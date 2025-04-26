from django.urls import path

from apps.statistics.views import CounterAgentListAPIView, HotelStatisticListAPIView, TransportStatisticListAPIView


urlpatterns = [
    # == Statistic URLs ===
    path("counter_agents/", CounterAgentListAPIView.as_view(), name="counter-agent-statistics"),
    path("hotels/", HotelStatisticListAPIView.as_view(), name="hotel-statistics"),
    path("transport/", TransportStatisticListAPIView.as_view(), name="transport-statistics"),
]