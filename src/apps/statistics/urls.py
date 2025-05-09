from django.urls import path

from apps.statistics.views import (CounterAgentListAPIView,
                                   HotelStatisticListAPIView,
                                   TransportStatisticListAPIView,
                                   HotelDiagramListAPIView,
                                   SectionStatisticListAPIView,
                                   FoodStatisticListAPIView,
                                   MenuStatisticListAPIView,
                                   RecipeStatisticListAPIView,
                                   CheckoutListAPIView,
                                   CheckInListAPIView,
                                   MostUsedProductsListAPIView,
                                   CheckInCheckoutDiagramAPIView,
                                   StatisticKitchenAPIView,
                                   HotelAndKitchenDiagramAPIView)


urlpatterns = [
    # ====================== Statistic URLs ======================
    path("counter_agents/", CounterAgentListAPIView.as_view(), name="counter-agent-statistics"),
    path("hotels/", HotelStatisticListAPIView.as_view(), name="hotel-statistics"),
    path("transports/", TransportStatisticListAPIView.as_view(), name="transport-statistics"),
    path("sections/", SectionStatisticListAPIView.as_view(), name="section-statistics"),
    path("foods/", FoodStatisticListAPIView.as_view(), name="food-statistics"),
    path("menus/", MenuStatisticListAPIView.as_view(), name="menu-statistics"),
    path("recipes/", RecipeStatisticListAPIView.as_view(), name="recipe-statistics"),
    path("checkout_products/", CheckoutListAPIView.as_view(), name="checkout-products-statistics"),
    path("check_in_products/", CheckInListAPIView.as_view(), name="check-in-products-statistics"),
    path("most_used_products/", MostUsedProductsListAPIView.as_view(), name="most-used-products-statistics"),
    path("kitchen/", StatisticKitchenAPIView.as_view(), name="kitchen-statistics"),
    # ====================== Diagram URLs ======================
    path("hotels-diagram/", HotelDiagramListAPIView.as_view(), name="hotel-statistics-diagram"),
    path("kitchen-diagram/", CheckInCheckoutDiagramAPIView.as_view(), name="kitchen-statistics-diagram"),
    path("kitchen-hotel-diagram/", HotelAndKitchenDiagramAPIView.as_view(), name="kitchen-hotel-statistics-diagram"),
]