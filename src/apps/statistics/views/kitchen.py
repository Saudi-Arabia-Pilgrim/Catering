import calendar

from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.foods.models import FoodSection, Food
from apps.orders.models import HotelOrder
from apps.menus.models import Menu, Recipe
from apps.orders.models import FoodOrder
from apps.statistics.utils import validate_from_and_date_to_date, iterate_months
from apps.statistics.views.abstract import AbstractStatisticsAPIView
from apps.warehouses.models import Warehouse


class SectionStatisticListAPIView(AbstractStatisticsAPIView):
    queryset = FoodSection.objects.all().prefetch_related("foods")

    def get(self, *args, **kwargs):
        sections = self.get_queryset()
        data = []
        for section in sections:
            section_data = {"name": section.name, "order_count": 0, "price": 0}
            if section.foods.exists():
                for food in section.foods.all():
                    section_data["order_count"] += food.orders.count()
                    if food.orders.exists:
                        for order in food.orders.all():
                            section_data["price"] += order.profit
            data.append(section_data)
        data.sort(
            key=lambda section_statistic: section_statistic["price"], reverse=True
        )
        return Response(data)


class FoodStatisticListAPIView(AbstractStatisticsAPIView):
    queryset = Food.objects.all().select_related("section").prefetch_related("orders")

    def get(self, request, *args, **kwargs):
        foods = self.get_queryset()
        data = []
        for food in foods:
            food_data = {
                "name": food.name,
                "order_count": food.orders.count(),
                "section": food.section.name,
                "price": 0,
                "image": (
                    request.build_absolute_uri(food.image.url) if food.image else None
                ),
            }
            if food.orders.exists():
                for order in food.orders.all():
                    food_data["price"] += order.profit
            data.append(food_data)
        data.sort(key=lambda food_data: food_data["price"], reverse=True)
        return Response(data)


class MenuStatisticListAPIView(AbstractStatisticsAPIView):
    queryset = Menu.objects.all().prefetch_related("orders")

    def get(self, request, *args, **kwargs):
        menus = self.get_queryset()
        data = []
        for menu in menus:
            menu_data = {
                "name": menu.name,
                "order_count": menu.orders.count(),
                "net_price": 0,
                "profit": 0,
                "gross_price": 0,
                "image": (
                    request.build_absolute_uri(menu.image.url) if menu.image else None
                ),
            }
            if menu.orders.exists():
                for order in menu.orders.all():
                    menu_data["net_price"] += order.net_price
                    menu_data["profit"] += order.profit
                    menu_data["gross_price"] += order.price
            data.append(menu_data)
        data.sort(key=lambda menu_data: menu_data["profit"], reverse=True)
        return Response(data)


class RecipeStatisticListAPIView(AbstractStatisticsAPIView):
    queryset = Recipe.objects.all().prefetch_related("orders")

    def get(self, request, *args, **kwargs):
        recipes = self.get_queryset()
        data = []
        total = 0
        for recipe in recipes:
            recipe_data = {
                "name": recipe.name,
                "order_count": recipe.orders.count(),
                "price": 0,
            }
            if recipe.orders.exists():
                for order in recipe.orders.all():
                    recipe_data["price"] += order.profit
                    total += order.profit
            data.append(recipe_data)
        data.sort(key=lambda recipe_data: recipe_data["price"], reverse=True)
        return Response({"total": total, "result": data})


class StatisticKitchenAPIView(CustomGenericAPIView):
    def get(self, request, *args, **kwargs):
        from_date, to_date = validate_from_and_date_to_date(request)

        warehouses = list(
            Warehouse.objects.filter(created_at__lte=to_date, created_at__gte=from_date)
        )
        orders = list(
            FoodOrder.objects.filter(
                created_at__lte=to_date, created_at__gte=from_date, status=True
            )
        )

        data = {"check_in": 0, "checkout": 0, "profit": 0, "general_trade": 0}

        for order in orders:
            data["checkout"] += order.price
            data["profit"] += order.profit

        for warehouse in warehouses:
            data["check_in"] += warehouse.gross_price

        data["general_trade"] = data["checkout"] - data["check_in"]

        return Response(data)


class HotelAndKitchenDiagramAPIView(CustomGenericAPIView):
    def get(self, request, *args, **kwargs):
        from_date, to_date = validate_from_and_date_to_date(request)

        data = []

        food_orders = list(
            FoodOrder.objects.filter(
                created_at__lte=to_date, created_at__gte=from_date, status=True
            )
        )
        hotel_orders = list(
            HotelOrder.objects.filter(
                created_at__lte=to_date,
                created_at__gte=from_date,
                order_status=HotelOrder.OrderStatus.COMPLETED,
            )
        )

        for month_date in iterate_months(from_date, to_date):

            month_hotel_orders = []
            month_food_orders = []
            month_name = calendar.month_name[month_date.month]

            for hotel_order in hotel_orders:
                if hotel_order.created_at.month == month_date.month:
                    month_hotel_orders.append(hotel_order)

            for food_order in food_orders:
                if food_order.created_at.month == month_date.month:
                    month_food_orders.append(food_order)

            diagram = {
                "name": month_name,
                "mehmonxona": {len(month_hotel_orders),},
                "ovqat": len(month_food_orders),
                }
            data.append(diagram)

        return Response(data)
