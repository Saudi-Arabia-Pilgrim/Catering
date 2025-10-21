"""
Missing Products Utility Module

This module provides functionality to calculate missing products for food items
when their status is False due to insufficient warehouse inventory.

The main function `calculate_missing_products_for_food` checks the warehouse
inventory against the required products for a food's recipes and returns
a dictionary of missing products with their quantities.

Example:
    missing_products = calculate_missing_products_for_food(food_instance)
    # Returns: {"Product Name": 5.25, "Another Product": 2.00}
"""

from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Sum, F, Case, When, DecimalField, Value
from apps.warehouses.models import Warehouse


def calculate_missing_products_for_food(food):
    """
    Calculate missing products for a food item based on actual warehouse inventory.

    This function checks the warehouse inventory against the required products
    for a food's recipes and returns a dictionary of missing products with
    their names and the quantities that are missing. It always calculates based
    on real quantities, regardless of food/product status.

    Args:
        food: A Food instance to check for missing products

    Returns:
        dict: A dictionary where keys are product names and values are the
              missing quantities (rounded to 2 decimal places)
              Example: {"Product Name": 5.25, "Another Product": 2.00}
    """
    missing_products = {}

    # Get all recipe foods for this food
    recipe_foods = food.recipes.all()

    if not recipe_foods:
        return missing_products

    # Step 1: Collect all products and sum up required quantities
    # Map: {product_id: total_required_quantity}
    products_required = {}
    product_objects = {}

    for recipe_food in recipe_foods:
        product_id = recipe_food.product_id
        required_qty = recipe_food.count

        # Sum up if product already exists (same product used multiple times)
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

    # Create a dictionary for quick lookup
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
            missing_products[product.name] = str(rounded_missing)

    return missing_products


def calculate_missing_products_batch(foods):
    """
    Calculate missing products for multiple food items in a single batch.
    This is more efficient than calling calculate_missing_products_for_food
    for each food individually. Always calculates based on real warehouse
    quantities, regardless of food/product status.

    Args:
        foods: QuerySet or list of Food instances

    Returns:
        dict: Dictionary mapping food IDs to their missing products
              Example: {food_id: {"Product Name": 5.25}, ...}
    """
    if not foods:
        return {}

    # Get all recipe foods for all foods
    all_recipe_foods = []
    food_recipe_mapping = {}

    for food in foods:
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

    # Calculate missing products for each food
    result = {}
    for food in foods:
        missing_products = {}
        recipe_foods = food_recipe_mapping[food.id]

        # Step 1: Sum up required quantities per product for this food
        products_required = {}
        product_objects = {}

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
                missing_products[product.name] = str(rounded_missing)

        result[food.id] = missing_products

    return result
