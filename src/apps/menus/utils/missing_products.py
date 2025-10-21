"""
Missing Products Utility Module for Menus and Recipes

This module provides functionality to calculate missing products for menu and recipe items
when their status is False due to insufficient warehouse inventory.

The main functions check warehouse inventory against the required products
for menus/recipes and return dictionaries of missing products with their quantities.
"""

from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Sum, F, Case, When, DecimalField, Value, Prefetch
from apps.warehouses.models import Warehouse
from apps.foods.models import Food, RecipeFood


def calculate_missing_products_for_menu(menu):
    """
    Calculate missing products for a menu item based on actual warehouse inventory.

    This function checks the warehouse inventory against the required products
    for all foods in the menu and returns a dictionary of missing products with
    their names, quantities, and measures. It always calculates based
    on real quantities, regardless of menu/food/product status.

    Args:
        menu: A Menu instance to check for missing products

    Returns:
        dict: A dictionary where keys are product names and values are dictionaries
              containing measure and missing quantity
              Example: {
                  "Product Name": {
                      "measure": "kg",
                      "missing": "5.25"
                  },
                  "Another Product": {
                      "measure": "L",
                      "missing": "2.00"
                  }
              }
    """
    missing_products = {}

    # Get all foods for this menu with prefetched recipe and product data
    foods = menu.foods.prefetch_related('recipes__product__measure').all()

    if not foods:
        return missing_products

    # Step 1: Collect all recipe_foods and sum up required quantities per product
    # Map: {product_id: total_required_quantity}
    products_required = {}
    product_objects = {}  # Map: {product_id: product_object}

    for food in foods:
        recipe_foods = food.recipes.all()
        for recipe_food in recipe_foods:
            product_id = recipe_food.product_id
            required_qty = recipe_food.count

            # Sum up if product already exists
            if product_id in products_required:
                products_required[product_id] += required_qty
            else:
                products_required[product_id] = required_qty
                product_objects[product_id] = recipe_food.product

    if not products_required:
        return missing_products

    # Step 2: Get warehouse data for all required products
    product_ids = list(products_required.keys())
    warehouse_data = (
        Warehouse.objects.filter(
            product_id__in=product_ids
        ).values('product_id').annotate(
            total_available=Sum(
                F("count")
                * Case(
                    When(product__difference_measures=0, then=Value(1)),
                    default=F("product__difference_measures"),
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                )
            )
        )
    )

    # Create warehouse lookup dictionary
    warehouse_dict = {item['product_id']: item['total_available'] or Decimal('0') for item in warehouse_data}

    # Step 3: Compare required vs available and calculate missing
    for product_id, required_quantity in products_required.items():
        total_available = warehouse_dict.get(product_id, Decimal('0'))
        missing_quantity = required_quantity - total_available

        if missing_quantity > 0:
            product = product_objects[product_id]
            # Round to 2 decimal places
            rounded_missing = Decimal(str(missing_quantity)).quantize(
                Decimal('0.01'),
                rounding=ROUND_HALF_UP
            )
            missing_products[product.name] = {
                "measure": product.measure.abbreviation,
                "missing": str(rounded_missing)
            }

    return missing_products


def calculate_missing_products_for_recipe(recipe):
    """
    Calculate missing products for a recipe item based on actual warehouse inventory.

    This function checks the warehouse inventory against the required products
    for all menus associated with the recipe and returns a dictionary of missing
    products with their names, quantities, and measures. It always
    calculates based on real quantities, regardless of recipe/menu/food/product status.

    Args:
        recipe: A Recipe instance to check for missing products

    Returns:
        dict: A dictionary where keys are product names and values are dictionaries
              containing measure and missing quantity
              Example: {
                  "Product Name": {
                      "measure": "kg",
                      "missing": "5.25"
                  },
                  "Another Product": {
                      "measure": "L",
                      "missing": "2.00"
                  }
              }
    """
    missing_products = {}

    # Get all menus associated with this recipe
    menus = [recipe.menu_breakfast, recipe.menu_lunch, recipe.menu_dinner]
    menus = [menu for menu in menus if menu]  # Get all non-null menus

    if not menus:
        return missing_products

    # Get all foods for all menus with prefetched recipe and product data
    all_foods = []
    for menu in menus:
        foods = menu.foods.prefetch_related('recipes__product__measure').all()
        all_foods.extend(foods)

    if not all_foods:
        return missing_products

    # Step 1: Collect all recipe_foods and sum up required quantities per product
    # Map: {product_id: total_required_quantity}
    products_required = {}
    product_objects = {}  # Map: {product_id: product_object}

    for food in all_foods:
        recipe_foods = food.recipes.all()
        for recipe_food in recipe_foods:
            product_id = recipe_food.product_id
            required_qty = recipe_food.count

            # Sum up if product already exists
            if product_id in products_required:
                products_required[product_id] += required_qty
            else:
                products_required[product_id] = required_qty
                product_objects[product_id] = recipe_food.product

    if not products_required:
        return missing_products

    # Step 2: Get warehouse data for all required products
    product_ids = list(products_required.keys())
    warehouse_data = (
        Warehouse.objects.filter(
            product_id__in=product_ids
        ).values('product_id').annotate(
            total_available=Sum(
                F("count")
                * Case(
                    When(product__difference_measures=0, then=Value(1)),
                    default=F("product__difference_measures"),
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                )
            )
        )
    )

    # Create warehouse lookup dictionary
    warehouse_dict = {item['product_id']: item['total_available'] or Decimal('0') for item in warehouse_data}

    # Step 3: Compare required vs available and calculate missing
    for product_id, required_quantity in products_required.items():
        total_available = warehouse_dict.get(product_id, Decimal('0'))
        missing_quantity = required_quantity - total_available

        if missing_quantity > 0:
            product = product_objects[product_id]
            # Round to 2 decimal places
            rounded_missing = Decimal(str(missing_quantity)).quantize(
                Decimal('0.01'),
                rounding=ROUND_HALF_UP
            )
            missing_products[product.name] = {
                "measure": product.measure.abbreviation,
                "missing": str(rounded_missing)
            }

    return missing_products


def calculate_missing_products_batch_menus(menus):
    """
    Calculate missing products for multiple menu items in a single batch.
    This is more efficient than calling calculate_missing_products_for_menu
    for each menu individually. Always calculates based on real warehouse
    quantities, regardless of menu/food/product status.

    Args:
        menus: QuerySet or list of Menu instances

    Returns:
        dict: Dictionary mapping menu IDs to their missing products
              Example: {
                  menu_id: {
                      "Product Name": {
                          "measure": "kg",
                          "missing": "5.25"
                      }
                  }
              }
    """
    if not menus:
        return {}

    # Get all foods for all menus with prefetched relations
    all_foods = []
    menu_food_mapping = {}

    for menu in menus:
        foods = list(menu.foods.prefetch_related('recipes__product__measure').all())
        all_foods.extend(foods)
        menu_food_mapping[menu.id] = foods

    if not all_foods:
        return {}

    # Get all recipe foods for all foods
    all_recipe_foods = []
    food_recipe_mapping = {}

    for food in all_foods:
        recipe_foods = list(food.recipes.all())
        all_recipe_foods.extend(recipe_foods)
        food_recipe_mapping[food.id] = recipe_foods

    if not all_recipe_foods:
        return {}

    # Get all unique product IDs
    product_ids = list(set(rf.product_id for rf in all_recipe_foods))

    # Batch query all warehouse data
    warehouse_data = (
        Warehouse.objects.filter(
            product_id__in=product_ids
        ).values('product_id').annotate(
            total_available=Sum(
                F("count")
                * Case(
                    When(product__difference_measures=0, then=Value(1)),
                    default=F("product__difference_measures"),
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                )
            )
        )
    )

    # Create warehouse lookup dictionary
    warehouse_dict = {item['product_id']: item['total_available'] or Decimal('0') for item in warehouse_data}

    # Calculate missing products for each menu
    result = {}
    for menu in menus:
        missing_products = {}
        foods = menu_food_mapping[menu.id]

        # Step 1: Sum up required quantities per product for this menu
        products_required = {}
        product_objects = {}

        for food in foods:
            recipe_foods = food_recipe_mapping[food.id]
            for recipe_food in recipe_foods:
                product_id = recipe_food.product_id
                required_qty = recipe_food.count

                if product_id in products_required:
                    products_required[product_id] += required_qty
                else:
                    products_required[product_id] = required_qty
                    product_objects[product_id] = recipe_food.product

        # Step 2: Compare with warehouse and calculate missing
        for product_id, required_quantity in products_required.items():
            total_available = warehouse_dict.get(product_id, Decimal('0'))
            missing_quantity = required_quantity - total_available

            if missing_quantity > 0:
                product = product_objects[product_id]
                rounded_missing = Decimal(str(missing_quantity)).quantize(
                    Decimal('0.01'),
                    rounding=ROUND_HALF_UP
                )
                missing_products[product.name] = {
                    "measure": product.measure.abbreviation,
                    "missing": str(rounded_missing)
                }

        result[menu.id] = missing_products

    return result


def calculate_missing_products_batch_recipes(recipes):
    """
    Calculate missing products for multiple recipe items in a single batch.
    This is more efficient than calling calculate_missing_products_for_recipe
    for each recipe individually. Always calculates based on real warehouse
    quantities, regardless of recipe/menu/food/product status.

    Args:
        recipes: QuerySet or list of Recipe instances

    Returns:
        dict: Dictionary mapping recipe IDs to their missing products
              Example: {
                  recipe_id: {
                      "Product Name": {
                          "measure": "kg",
                          "missing": "5.25"
                      }
                  }
              }
    """
    if not recipes:
        return {}

    # Get all menus for all recipes
    all_menus = []
    recipe_menu_mapping = {}

    for recipe in recipes:
        menus = [recipe.menu_breakfast, recipe.menu_lunch, recipe.menu_dinner]
        menus = [menu for menu in menus if menu]  # Get all non-null menus
        all_menus.extend(menus)
        recipe_menu_mapping[recipe.id] = menus

    if not all_menus:
        return {}

    # Get all foods for all menus with prefetched relations
    all_foods = []
    menu_food_mapping = {}

    for menu in all_menus:
        foods = list(menu.foods.prefetch_related('recipes__product__measure').all())
        all_foods.extend(foods)
        menu_food_mapping[menu.id] = foods

    if not all_foods:
        return {}

    # Get all recipe foods for all foods
    all_recipe_foods = []
    food_recipe_mapping = {}

    for food in all_foods:
        recipe_foods = list(food.recipes.all())
        all_recipe_foods.extend(recipe_foods)
        food_recipe_mapping[food.id] = recipe_foods

    if not all_recipe_foods:
        return {}

    # Get all unique product IDs
    product_ids = list(set(rf.product_id for rf in all_recipe_foods))

    # Batch query all warehouse data
    warehouse_data = (
        Warehouse.objects.filter(product_id__in=product_ids)
        .values("product_id")
        .annotate(
            total_available=Sum(
                F("count")
                * Case(
                    When(product__difference_measures=0, then=Value(1)),
                    default=F("product__difference_measures"),
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                )
            )
        )
    )

    # Create warehouse lookup dictionary
    warehouse_dict = {item['product_id']: item['total_available'] or Decimal('0') for item in warehouse_data}

    # Calculate missing products for each recipe
    result = {}
    for recipe in recipes:
        missing_products = {}
        menus = recipe_menu_mapping[recipe.id]

        # Step 1: Sum up required quantities per product for this recipe
        products_required = {}
        product_objects = {}

        for menu in menus:
            foods = menu_food_mapping[menu.id]
            for food in foods:
                recipe_foods = food_recipe_mapping[food.id]
                for recipe_food in recipe_foods:
                    product_id = recipe_food.product_id
                    required_qty = recipe_food.count

                    if product_id in products_required:
                        products_required[product_id] += required_qty
                    else:
                        products_required[product_id] = required_qty
                        product_objects[product_id] = recipe_food.product

        # Step 2: Compare with warehouse and calculate missing
        for product_id, required_quantity in products_required.items():
            total_available = warehouse_dict.get(product_id, Decimal('0'))
            missing_quantity = required_quantity - total_available

            if missing_quantity > 0:
                product = product_objects[product_id]
                rounded_missing = Decimal(str(missing_quantity)).quantize(
                    Decimal('0.01'),
                    rounding=ROUND_HALF_UP
                )
                missing_products[product.name] = {
                    "measure": product.measure.abbreviation,
                    "missing": str(rounded_missing)
                }

        result[recipe.id] = missing_products

    return result
