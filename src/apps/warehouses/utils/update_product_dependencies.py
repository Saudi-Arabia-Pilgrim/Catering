from decimal import Decimal

from django.db.models import Q
from django.apps import apps

from apps.products.models import Product
from apps.foods.models import Food
from apps.menus.models import Menu, Recipe


def update_product_dependencies_in_warehouse(product_ids: list):
    Warehouse = apps.get_model("warehouses", "Warehouse")
    RecipeFood = apps.get_model("foods", "RecipeFood")
    product_list = []
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

    for warehouse in warehouse_qs:
        product_list.append(warehouse.product)

    for product in product_list:
        if warehouse.count > Decimal('0'):
            product.status = True
        else:
            product.status = False

    for product_id in product_ids:
        warehouses_dict[product_id] = warehouse_qs.filter(product_id=product_id)

    for recipe_food in recipe_food_qs:
        product_id = recipe_food.product_id
        recipe_food.calculate_prices(warehouse=warehouses_dict[product_id])
        product_count = sum([w.count for w in warehouses_dict[product_id]])
        product = recipe_food.product
        # Calculate actual available quantity considering difference_measures
        available_quantity = product_count * (product.difference_measures if product.difference_measures else Decimal('1'))
        if product_count == Decimal('0') or recipe_food.count > available_quantity:
            recipe_food.status = False
        else:
            recipe_food.status = True

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

    Product.objects.bulk_update(product_list, ["status"])
    RecipeFood.objects.bulk_update(recipe_food_qs, ["status", "price"])
    Food.objects.bulk_update(food_qs, ["status", "net_price", "gross_price"])
    Menu.objects.bulk_update(menu_qs, ["status", "net_price", "gross_price"])
    Recipe.objects.bulk_update(recipe_qs, ["status", "net_price", "gross_price"])
