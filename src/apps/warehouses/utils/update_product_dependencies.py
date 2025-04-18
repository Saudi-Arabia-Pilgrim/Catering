from django.db.models import Q

from apps.foods.models import Food, RecipeFood
from apps.menus.models.menu import Menu
from apps.menus.models.recipe import Recipe
from apps.warehouses.models import Warehouse


def update_product_dependencies_in_warehouse(product_ids: list):
    recipe_food_qs = RecipeFood.objects.filter(product_id__in=product_ids)
    food_qs = Food.objects.filter(recipes__in=recipe_food_qs).prefetch_related(
        "recipes"
    ).distinct()
    menu_qs = Menu.objects.filter(foods__in=food_qs).distinct().prefetch_related("foods")
    recipe_qs = Recipe.objects.filter(
        Q(menu_breakfast__in=menu_qs)
        | Q(menu_lunch__in=menu_qs)
        | Q(menu_dinner__in=menu_qs)
    ).distinct().select_related("menu_breakfast", "menu_lunch", "menu_dinner")
    warehouse_qs = Warehouse.objects.filter(product_id__in=product_ids).select_related(
        "product"
    )
    warehouses_dict = {}

    for product_id in product_ids:
        warehouses_dict[product_id] = warehouse_qs.filter(product_id=product_id)

    for recipe_food in recipe_food_qs:
        product_id = recipe_food.product_id
        recipe_food.calculate_prices(warehouse=warehouses_dict[product_id])
        product_count = sum([w.count for w in warehouses_dict[product_id]])
        if product_count > recipe_food.count:
            recipe_food.status = True
        else:
            recipe_food.status = False

    for food in food_qs:
        recipes = food.recipes.all()
        food.calculate_prices(recipes)
        food.check_status(recipes)

    for menu in menu_qs:
        foods = menu.foods.all()
        menu.calculate_prices(foods)
        menu.change_status(foods)

    for recipe in recipe_qs:
        status = all(
            [
                recipe.menu_breakfast.status,
                recipe.menu_lunch.status,
                recipe.menu_dinner.status,
            ]
        )
        recipe.calculate_prices()
        recipe.status = status

    RecipeFood.objects.bulk_update(recipe_food_qs, ["status", "price"])
    Food.objects.bulk_update(food_qs, ["status", "net_price", "gross_price"])
    Menu.objects.bulk_update(menu_qs, ["status", "net_price", "gross_price"])
    Recipe.objects.bulk_update(recipe_qs, ["status", "net_price", "gross_price"])
