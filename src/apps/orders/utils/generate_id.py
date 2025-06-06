import random

from django.apps import apps


def new_id():
    """
    Generate a new unique ID for a HotelOrder.

    This function generates a random 8-digit integer and checks if it already
    exists as a food_order_id in the HotelOrder model. If the generated ID
    already exists, the function recursively calls itself to generate a new ID
    until a unique one is found.

    Returns:
        str: A unique 8-digit ID as a string.
    """
    HotelOrder = apps.get_model("orders", "HotelOrder")
    pk = random.randint(10000000, 99999999)
    if HotelOrder.objects.filter(order_id=pk).exists():
        return new_id()
    return str(pk)
