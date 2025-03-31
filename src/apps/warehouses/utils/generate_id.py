import random

from django.apps import apps


def new_id():
    Warehouse = apps.get_model('warehouses', 'Warehouse')
    pk = random.randint(10000000, 99999999)
    if Warehouse.objects.filter(warehouse_id=pk).exists():
        return new_id()
    return str(pk)