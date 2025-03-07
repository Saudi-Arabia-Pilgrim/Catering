import random

from django.apps import apps


def new_id():
    FoodOrder = apps.get_model('orders', 'FoodOrder')  # Динамический импорт
    pk = random.randint(10000000, 99999999)
    if FoodOrder.objects.filter(food_order_id=pk).exists():
        return new_id()
    return str(pk)