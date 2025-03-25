from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Exists, Q, Sum, OuterRef

from apps.menus.models import Recipe
from apps.warehouses.models import Warehouse
from apps.menus.models import Menu
from apps.foods.models import Food, RecipeFood


@receiver(post_save, sender=Warehouse)
def post_save_warehouse(sender, instance, created, **kwargs):
    product = instance.product
    product_count_in_warehouse = Warehouse.objects.filter(product=product).aggregate(total=Sum('count'))['total'] or 0
    product_count = (product_count_in_warehouse * product.difference_measures) if product.difference_measures > 0 else product_count_in_warehouse

    with transaction.atomic():
        if product_count > 0:
            product.status = True

            food_recipes = list(RecipeFood.objects.filter(product=product))
            recipes_status = {"False": [], "True": []}

            warehouse = food_recipes[0].get_product_in_warehouse() if food_recipes[0] else None
            for food_recipe in food_recipes:
                food_recipe.status = food_recipe.count <= product_count
                recipes_status["True" if food_recipe.status else "False"].append(food_recipe.id)
                food_recipe.calculate_prices(warehouse)

            RecipeFood.objects.bulk_update(food_recipes, ['status', 'price'])

            active_foods = Food.objects.filter(recipes__id__in=recipes_status["True"]).annotate(
                has_inactive_recipes=Exists(RecipeFood.objects.filter(food=OuterRef("pk"), status=False))).prefetch_related("recipes")
            inactive_foods = Food.objects.filter(recipes__id__in=recipes_status["False"]).prefetch_related("recipes")

            for food in active_foods:
                food.status = not food.has_inactive_recipes
                food.calculate_prices()
            for food in inactive_foods:
                food.status = False
                food.calculate_prices()

            Food.objects.bulk_update(list(active_foods) + list(inactive_foods), ['status', 'net_price', 'gross_price'])

            active_menus = Menu.objects.filter(foods__in=active_foods.filter(status=True)).annotate(
                has_inactive_food=Exists(Food.objects.filter(menus=OuterRef("pk"), status=False))
            ).prefetch_related("foods")
            inactive_menus = Menu.objects.filter(foods__in=active_foods.filter(status=False) | inactive_foods).prefetch_related("foods")

            for menu in active_menus:
                menu.status = not menu.has_inactive_food
                menu.calculate_prices()
            for menu in inactive_menus:
                menu.status = False
                menu.calculate_prices()

            Menu.objects.bulk_update(list(inactive_menus) + list(active_menus), ['status', 'net_price', 'gross_price'])

            active_menus = active_menus.filter(status=True)
            inactive_menus = Menu.objects.filter(id__in=active_menus.filter(status=False) | inactive_menus)

            active_recipes = Recipe.objects.filter(
                Q(menu_breakfast__in=active_menus) |
                Q(menu_lunch__in=active_menus) |
                Q(menu_dinner__in=active_menus)
            ).annotate(
                has_inactive_menu=Exists(
                    Menu.objects.filter(
                        OuterRef("menu_breakfast"),
                        status=False
                    ) | Menu.objects.filter(
                        OuterRef("menu_lunch"),
                        status=False
                    ) | Menu.objects.filter(
                        OuterRef("menu_dinner"),
                        status=False
                    )
                )
            )
            inactive_recipes = Recipe.objects.filter(
                Q(menu_breakfast__in=inactive_menus) |
                Q(menu_lunch__in=inactive_menus) |
                Q(menu_dinner__in=inactive_menus)
            )

            for recipe in active_recipes:
                recipe.status = not recipe.has_inactive_menu
                recipe.calculate_prices()
            for recipe in inactive_recipes:
                recipe.status = False
                recipe.calculate_prices()

            Recipe.objects.bulk_update(list(active_recipes) + list(inactive_recipes), ['status', 'slug', 'net_price', 'gross_price'])

        else:
            product.status = False

            recipe_foods = RecipeFood.objects.filter(product=product)
            foods = Food.objects.filter(recipes__in=recipe_foods).distinct()
            menus = Menu.objects.filter(foods__in=foods).distinct()
            recipes = Recipe.objects.filter(
                Q(menu_breakfast__in=menus) |
                Q(menu_lunch__in=menus) |
                Q(menu_dinner__in=menus)
            ).distinct()

            for obj in list(recipe_foods) + list(foods) + list(menus) + list(recipes):
                obj.status = False

            RecipeFood.objects.bulk_update(recipe_foods, ['status', 'price'])
            Food.objects.bulk_update(foods, ['status', 'slug', 'net_price', 'gross_price'])
            Menu.objects.bulk_update(menus, ['status', 'slug', 'net_price', 'gross_price'])
            Recipe.objects.bulk_update(recipes, ['status', 'slug', 'net_price', 'gross_price'])

        product.save()