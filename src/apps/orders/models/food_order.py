from django.db import models

from apps.base.models import AbstractBaseModel


class FoodOrder(AbstractBaseModel):
    """
    Model representing a food order.

    Attributes:

        menu (ForeignKey): 
        recipe (ForeignKey):
        hotel (ForeignKey):
        order_time (DateTimeField): 
        expiration_date (DateTimeField): 
        order_type (PositiveSmallIntegerField):
        product_type (PositiveSmallIntegerField): 
        price (DecimalField):
        address (CharField):
        product_count (PositiveSmallIntegerField): 

    Meta:
        db_table (str): 
        verbose_name (str): 
        verbose_name_plural (str): 

    Methods:
        __str__(): 
    """

    class OrderType(models.IntegerChoices):
        CONTINUOUS = 0, 'Davomiy'
        ONCE = 1, 'Bir martalik'

    class ProductType(models.IntegerChoices):
        FOOD = 0, 'Ovqat'
        MENU = 1, 'Menu'
        RECIPE = 2, 'Retsept'

    # === Unique identifier for the food order. ===
    food_order_id = models.CharField(default="apps.orders.utils.generate_id.pynew_id", max_length=24, unique=True)
    # === Reference to the food item being ordered. ===
    food = models.ForeignKey('foods.Food', on_delete=models.PROTECT, related_name='food_orders', blank=True, null=True)
    # === Reference to the menu being ordered. ===
    menu = models.ForeignKey('menus.Menu', on_delete=models.PROTECT, related_name='food_orders', blank=True, null=True)
    # === Reference to the recipe being ordered. ===
    recipe = models.ForeignKey('menus.Recipe', on_delete=models.PROTECT, related_name='food_orders', blank=True, null=True)

    # === Reference to the hotel associated with the order. ===
    hotel = models.ForeignKey('hotels.Hotel', on_delete=models.PROTECT, related_name='food_orders', blank=True, null=True)

    # === The time when the order was placed. ===
    order_time = models.DateTimeField(blank=True, null=True)    
    # === The expiration date of the order. ===
    expiration_date = models.DateTimeField(blank=True, null=True)

    # === The type of order (continuous or once). ===
    order_type = models.PositiveSmallIntegerField(choices=OrderType.choices)
    # === The type of product (food, menu, or recipe). ===
    product_type = models.PositiveSmallIntegerField(choices=ProductType.choices)

    # === The price of the order. ===
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # ===  The address where the order should be delivered. ===
    address = models.CharField(max_length=1200)

    # === The number of products in the order. ===
    product_count = models.PositiveSmallIntegerField()

    class Meta:
        # === The name of the database table. ===
        db_table = 'food_order'
        # === The human-readable name of the model. ===
        verbose_name = 'Food order'
        # === The human-readable plural name of the model. ===
        verbose_name_plural = 'Food orders'

    def __str__(self):
        """
        Returns a string representation of the food order.
        """
        return f"{self.food_order_id} - {self.get_order_type_display()} - {self.price}"