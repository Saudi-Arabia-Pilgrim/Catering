"""
Product Availability Check Utility Module

This module provides functions to check if there are enough products in warehouse
to fulfill requirements for Food, Menu, and Recipe items.

All functions check actual warehouse quantities rather than relying on status flags.
"""

from decimal import Decimal
from django.apps import apps
from django.db.models import Sum, F, Case, When, DecimalField, Value

Warehouse = None


def get_warehouse_model():
    global Warehouse
    if Warehouse is None:
        Warehouse = apps.get_model("warehouses", "Warehouse")
    return Warehouse


def check_food_availability(food):
    """
    Check if warehouse has enough products to fulfill a food item's requirements.

    This function calculates the total required quantity for all products used in
    the food's recipes and compares with actual warehouse availability.

    Args:
        food: A Food instance to check

    Returns:
        bool: True if all required products are available in sufficient quantity,
              False otherwise
    """
    Warehouse = get_warehouse_model()
    # Get all recipe foods for this food
    recipe_foods = food.recipes.all()

    if not recipe_foods:
        return True  # No products required, food is available

    # Step 1: Sum up required quantities per product
    products_required = {}

    for recipe_food in recipe_foods:
        product_id = recipe_food.product_id
        required_qty = recipe_food.count

        if product_id in products_required:
            products_required[product_id] += required_qty
        else:
            products_required[product_id] = required_qty

    if not products_required:
        return True

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

    warehouse_dict = {
        item['product_id']: item['total_available'] or Decimal('0')
        for item in warehouse_data
    }

    # Step 3: Check if all products are available in sufficient quantity
    for product_id, required_quantity in products_required.items():
        total_available = warehouse_dict.get(product_id, Decimal('0'))
        if required_quantity > total_available:
            return False  # Not enough of this product

    return True  # All products are available


def check_menu_availability(menu):
    """
    Check if warehouse has enough products to fulfill a menu item's requirements.

    This function calculates the total required quantity for all products used in
    all foods of the menu and compares with actual warehouse availability.

    Args:
        menu: A Menu instance to check

    Returns:
        bool: True if all required products are available in sufficient quantity,
              False otherwise
    """
    Warehouse = get_warehouse_model()
    # Get all foods for this menu
    foods = menu.foods.all()

    if not foods:
        return True  # No foods, menu is available

    # Step 1: Sum up required quantities per product from all foods
    products_required = {}

    for food in foods:
        recipe_foods = food.recipes.all()
        for recipe_food in recipe_foods:
            product_id = recipe_food.product_id
            required_qty = recipe_food.count

            if product_id in products_required:
                products_required[product_id] += required_qty
            else:
                products_required[product_id] = required_qty

    if not products_required:
        return True

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

    warehouse_dict = {
        item['product_id']: item['total_available'] or Decimal('0')
        for item in warehouse_data
    }

    # Step 3: Check if all products are available in sufficient quantity
    for product_id, required_quantity in products_required.items():
        total_available = warehouse_dict.get(product_id, Decimal('0'))
        if required_quantity > total_available:
            return False

    return True


def check_recipe_availability(recipe):
    """
    Check if warehouse has enough products to fulfill a recipe item's requirements.

    This function calculates the total required quantity for all products used in
    all menus (breakfast, lunch, dinner) of the recipe and compares with actual
    warehouse availability.

    Args:
        recipe: A Recipe instance to check

    Returns:
        bool: True if all required products are available in sufficient quantity,
              False otherwise
    """
    Warehouse = get_warehouse_model()
    # Get all menus associated with this recipe
    menus = [recipe.menu_breakfast, recipe.menu_lunch, recipe.menu_dinner]
    menus = [menu for menu in menus if menu]

    if not menus:
        return True  # No menus, recipe is available

    # Step 1: Sum up required quantities per product from all menus
    products_required = {}

    for menu in menus:
        foods = menu.foods.all()
        for food in foods:
            recipe_foods = food.recipes.all()
            for recipe_food in recipe_foods:
                product_id = recipe_food.product_id
                required_qty = recipe_food.count

                if product_id in products_required:
                    products_required[product_id] += required_qty
                else:
                    products_required[product_id] = required_qty

    if not products_required:
        return True

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

    warehouse_dict = {
        item['product_id']: item['total_available'] or Decimal('0')
        for item in warehouse_data
    }

    # Step 3: Check if all products are available in sufficient quantity
    for product_id, required_quantity in products_required.items():
        total_available = warehouse_dict.get(product_id, Decimal('0'))
        if required_quantity > total_available:
            return False

    return True


def check_foods_availability_batch(foods):
    """
    Check availability for multiple food items in a single batch operation.
    This is more efficient than checking each food individually.

    Args:
        foods: QuerySet or list of Food instances

    Returns:
        dict: Dictionary mapping food IDs to their availability status (True/False)
              Example: {food_id: True, another_food_id: False, ...}
    """
    Warehouse = get_warehouse_model()
    if not foods:
        return {}

    # Collect all recipe foods and build mapping
    all_recipe_foods = []
    food_recipe_mapping = {}

    for food in foods:
        recipe_foods = list(food.recipes.all())
        all_recipe_foods.extend(recipe_foods)
        food_recipe_mapping[food.id] = recipe_foods

    if not all_recipe_foods:
        return {food.id: True for food in foods}

    # Get all unique product IDs
    product_ids = list(set(rf.product_id for rf in all_recipe_foods))

    # Batch query warehouse data
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

    warehouse_dict = {
        item['product_id']: item['total_available'] or Decimal('0')
        for item in warehouse_data
    }

    # Check availability for each food
    result = {}
    for food in foods:
        recipe_foods = food_recipe_mapping[food.id]

        # Sum up required quantities for this food
        products_required = {}
        for recipe_food in recipe_foods:
            product_id = recipe_food.product_id
            required_qty = recipe_food.count

            if product_id in products_required:
                products_required[product_id] += required_qty
            else:
                products_required[product_id] = required_qty

        # Check if all products are available
        is_available = True
        for product_id, required_quantity in products_required.items():
            total_available = warehouse_dict.get(product_id, Decimal('0'))
            if required_quantity > total_available:
                is_available = False
                break

        result[food.id] = is_available

    return result


def check_menus_availability_batch(menus):
    """
    Check availability for multiple menu items in a single batch operation.
    This is more efficient than checking each menu individually.

    Args:
        menus: QuerySet or list of Menu instances

    Returns:
        dict: Dictionary mapping menu IDs to their availability status (True/False)
              Example: {menu_id: True, another_menu_id: False, ...}
    """
    Warehouse = get_warehouse_model()
    if not menus:
        return {}

    # Collect all foods and recipe foods
    all_foods = []
    menu_food_mapping = {}

    for menu in menus:
        foods = list(menu.foods.all())
        all_foods.extend(foods)
        menu_food_mapping[menu.id] = foods

    if not all_foods:
        return {menu.id: True for menu in menus}

    # Get all recipe foods
    all_recipe_foods = []
    food_recipe_mapping = {}

    for food in all_foods:
        recipe_foods = list(food.recipes.all())
        all_recipe_foods.extend(recipe_foods)
        food_recipe_mapping[food.id] = recipe_foods

    if not all_recipe_foods:
        return {menu.id: True for menu in menus}

    # Get warehouse data
    product_ids = list(set(rf.product_id for rf in all_recipe_foods))
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

    warehouse_dict = {
        item['product_id']: item['total_available'] or Decimal('0')
        for item in warehouse_data
    }

    # Check availability for each menu
    result = {}
    for menu in menus:
        foods = menu_food_mapping[menu.id]

        # Sum up required quantities for this menu
        products_required = {}
        for food in foods:
            recipe_foods = food_recipe_mapping[food.id]
            for recipe_food in recipe_foods:
                product_id = recipe_food.product_id
                required_qty = recipe_food.count

                if product_id in products_required:
                    products_required[product_id] += required_qty
                else:
                    products_required[product_id] = required_qty

        # Check if all products are available
        is_available = True
        for product_id, required_quantity in products_required.items():
            total_available = warehouse_dict.get(product_id, Decimal('0'))
            if required_quantity > total_available:
                is_available = False
                break

        result[menu.id] = is_available

    return result


def check_recipes_availability_batch(recipes):
    """
    Check availability for multiple recipe items in a single batch operation.
    This is more efficient than checking each recipe individually.

    Args:
        recipes: QuerySet or list of Recipe instances

    Returns:
        dict: Dictionary mapping recipe IDs to their availability status (True/False)
              Example: {recipe_id: True, another_recipe_id: False, ...}
    """
    Warehouse = get_warehouse_model()
    if not recipes:
        return {}

    # Collect all menus
    all_menus = []
    recipe_menu_mapping = {}

    for recipe in recipes:
        menus = [recipe.menu_breakfast, recipe.menu_lunch, recipe.menu_dinner]
        menus = [menu for menu in menus if menu]
        all_menus.extend(menus)
        recipe_menu_mapping[recipe.id] = menus

    if not all_menus:
        return {recipe.id: True for recipe in recipes}

    # Collect all foods
    all_foods = []
    menu_food_mapping = {}

    for menu in all_menus:
        foods = list(menu.foods.all())
        all_foods.extend(foods)
        menu_food_mapping[menu.id] = foods

    if not all_foods:
        return {recipe.id: True for recipe in recipes}

    # Get all recipe foods
    all_recipe_foods = []
    food_recipe_mapping = {}

    for food in all_foods:
        recipe_foods = list(food.recipes.all())
        all_recipe_foods.extend(recipe_foods)
        food_recipe_mapping[food.id] = recipe_foods

    if not all_recipe_foods:
        return {recipe.id: True for recipe in recipes}

    # Get warehouse data
    product_ids = list(set(rf.product_id for rf in all_recipe_foods))
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

    warehouse_dict = {
        item['product_id']: item['total_available'] or Decimal('0')
        for item in warehouse_data
    }

    # Check availability for each recipe
    result = {}
    for recipe in recipes:
        menus = recipe_menu_mapping[recipe.id]

        # Sum up required quantities for this recipe
        products_required = {}
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

        # Check if all products are available
        is_available = True
        for product_id, required_quantity in products_required.items():
            total_available = warehouse_dict.get(product_id, Decimal('0'))
            if required_quantity > total_available:
                is_available = False
                break

        result[recipe.id] = is_available

    return result
