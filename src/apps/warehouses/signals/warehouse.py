from decimal import Decimal

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q, Sum

from apps.menus.models import Recipe
from apps.warehouses.models import Warehouse
from apps.menus.models import Menu
from apps.foods.models import Food, RecipeFood
from apps.warehouses.utils.check_availability import (
    check_foods_availability_batch,
    check_menus_availability_batch,
    check_recipes_availability_batch,
)


@receiver(post_save, sender=Warehouse)
def post_save_warehouse(sender, instance, created, **kwargs):
    """
    Signal handler that updates product, recipe_food, food, menu, and recipe statuses
    when warehouse changes. Status is determined by checking actual warehouse quantities
    rather than relying on status flags of dependent objects.
    """
    product = instance.product

    # Calculate total product count in warehouse
    product_count_in_warehouse = (
        Warehouse.objects.filter(product=product).aggregate(total=Sum("count"))["total"]
        or Decimal('0')
    )

    # Apply difference_measures to get actual available quantity
    difference_measures = product.difference_measures if product.difference_measures > Decimal('0') else Decimal('1')
    product_count = product_count_in_warehouse * difference_measures

    with transaction.atomic():
        # Update product status based on warehouse count
        product.status = product_count > Decimal('0')
        product.save()

        # Get all recipe_foods that use this product
        recipe_foods = RecipeFood.objects.filter(product=product).select_related('product')

        if not recipe_foods:
            return

        # Update RecipeFood statuses and prices
        warehouse_qs = (
            recipe_foods.first().get_product_in_warehouse()
            if recipe_foods.first()
            else None
        )

        for recipe_food in recipe_foods:
            # Check if warehouse has enough for this recipe_food
            recipe_food.status = recipe_food.count <= product_count
            if warehouse_qs:
                recipe_food.calculate_prices(warehouse_qs[0])

        RecipeFood.objects.bulk_update(recipe_foods, ["status", "price"])

        # Get all affected foods
        foods = Food.objects.filter(
            recipes__in=recipe_foods
        ).distinct().prefetch_related("recipes")

        if foods:
            # Check availability for all foods using batch function
            food_availability = check_foods_availability_batch(foods)

            # Update food statuses and prices
            for food in foods:
                food.status = food_availability.get(food.id, False)
                food.calculate_prices()

            Food.objects.bulk_update(
                foods,
                ["status", "net_price", "gross_price"],
            )

            # Get all affected menus
            menus = Menu.objects.filter(
                foods__in=foods
            ).distinct().prefetch_related("foods__recipes")

            if menus:
                # Check availability for all menus using batch function
                menu_availability = check_menus_availability_batch(menus)

                # Update menu statuses and prices
                for menu in menus:
                    menu.status = menu_availability.get(menu.id, False)
                    menu.calculate_prices()

                Menu.objects.bulk_update(
                    menus,
                    ["status", "net_price", "gross_price"],
                )

                # Get all affected recipes
                recipes = Recipe.objects.filter(
                    Q(menu_breakfast__in=menus)
                    | Q(menu_lunch__in=menus)
                    | Q(menu_dinner__in=menus)
                ).distinct().select_related(
                    "menu_breakfast", "menu_lunch", "menu_dinner"
                )

                if recipes:
                    # Prefetch foods and recipes for all menus used in recipes
                    for recipe in recipes:
                        if recipe.menu_breakfast:
                            recipe.menu_breakfast.foods.all()
                        if recipe.menu_lunch:
                            recipe.menu_lunch.foods.all()
                        if recipe.menu_dinner:
                            recipe.menu_dinner.foods.all()

                    # Check availability for all recipes using batch function
                    recipe_availability = check_recipes_availability_batch(recipes)

                    # Update recipe statuses and prices
                    for recipe in recipes:
                        recipe.status = recipe_availability.get(recipe.id, False)
                        recipe.calculate_prices()

                    Recipe.objects.bulk_update(
                        recipes,
                        ["status", "slug", "net_price", "gross_price"],
                    )
