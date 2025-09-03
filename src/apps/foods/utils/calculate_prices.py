from django.db.models import Q
from django.db import transaction
from django.apps import apps


class CalculatePrices:
    @classmethod
    def calculate_objects(cls, objs, type):
        with transaction.atomic():
            match type:
                case "recipe_food":
                    cls.calculate_foods(objs)
                    menus = cls.get_menus(objs)
                    cls.calculate_menus(menus)
                    cls.calculate_recipes(cls.get_recipes(menus))
                case "food":
                    cls.calculate_menus(objs)
                    cls.calculate_recipes(cls.get_recipes(objs))
                case "menu":
                    cls.calculate_recipes(objs)

    @classmethod
    def get_menus(cls, foods):
        Menu = apps.get_model("menus", "Menu")
        menus = list(
            Menu.objects.filter(foods__in=foods).prefetch_related("foods").distinct()
        )
        return menus

    @classmethod
    def get_recipes(cls, menus):
        Recipe = apps.get_model("menus", "Recipe")
        recipes = list(
            Recipe.objects.filter(
                Q(menu_breakfast__in=menus)
                | Q(menu_lunch__in=menus)
                | Q(menu_dinner__in=menus)
            ).distinct()
        )
        return recipes

    @classmethod
    def calculate_foods(cls, foods):
        Food = apps.get_model("foods", "Food")
        for food in foods:
            food.change_object()
        Food.objects.bulk_update(
            foods, ["status", "net_price", "profit", "gross_price"]
        )

    @classmethod
    def calculate_menus(cls, menus):
        Menu = apps.get_model("menus", "Menu")
        for menu in menus:
            menu.change_object()
        Menu.objects.bulk_update(
            menus, ["status", "net_price", "profit", "gross_price"]
        )

    @classmethod
    def calculate_recipes(cls, recipes):
        Recipe = apps.get_model("menus", "Recipe")
        for recipe in recipes:
            recipe.calculate_prices()
        Recipe.objects.bulk_update(
            recipes, ["status", "net_price", "profit", "gross_price"]
        )
