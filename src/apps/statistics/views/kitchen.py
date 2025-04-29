from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.foods.models import FoodSection, Food
from apps.menus.models import Menu, Recipe


class SectionStatisticListAPIView(CustomGenericAPIView):
    def get(self, *args, **kwargs):
        sections = FoodSection.objects.all().prefetch_related("foods")
        data = []
        for section in sections:
            section_data = {
                "name": section.name,
                "order_count": 0,
                "price": 0
            }
            if section.foods.exists():
                for food in section.foods.all():
                    section_data["order_count"] += food.orders.count()
                    if food.orders.exists:
                        for order in food.orders.all():
                            section_data["price"] += order.profit
            data.append(section_data)
        data.sort(key=lambda section_statistic: section_statistic["price"], reverse=True)
        return Response(data)


class FoodStatisticListAPIView(CustomGenericAPIView):
    def get(self, request,*args, **kwargs):
        foods = Food.objects.all().select_related("section").prefetch_related("orders")
        data = []
        for food in foods:
            food_data = {
                "name": food.name,
                "order_count": food.orders.count(),
                "section": food.section.name,
                "price": 0,
                "image": request.build_absolute_uri(food.image.url) if food.image else None
            }
            if food.orders.exists():
                for order in food.orders.all():
                    food_data["price"] += order.profit
            data.append(food_data)
        data.sort(key=lambda food_data: food_data["price"], reverse=True)
        return Response(data)


class MenuStatisticListAPIView(CustomGenericAPIView):
    def get(self, request,*args, **kwargs):
        menus = Menu.objects.all().prefetch_related("orders")
        data = []
        for menu in menus:
            menu_data = {
                "name": menu.name,
                "order_count": menu.orders.count(),
                "net_price": 0,
                "profit": 0,
                "gross_price": 0,
                "image": request.build_absolute_uri(menu.image.url) if menu.image else None
            }
            if menu.orders.exists():
                for order in menu.orders.all():
                    menu_data["net_price"] += order.net_price
                    menu_data["profit"] += order.profit
                    menu_data["gross_price"] += order.price
            data.append(menu_data)
        data.sort(key=lambda menu_data: menu_data["profit"], reverse=True)
        return Response(data)


class RecipeStatisticListAPIView(CustomGenericAPIView):
    def get(self, request,*args, **kwargs):
        recipes = Recipe.objects.all().prefetch_related("orders")
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