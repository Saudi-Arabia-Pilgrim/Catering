from django.db import models

from apps.base.exceptions import CustomExceptionError
from apps.base.models import AbstractBaseModel
from apps.orders.utils.generate_id import new_id


class FoodOrder(AbstractBaseModel):
    """
    Model representing a food order.
    """

    class OrderType(models.IntegerChoices):
        CONTINUOUS = 0, 'Davomiy'
        ONCE = 1, 'Bir martalik'

    class ProductType(models.IntegerChoices):
        FOOD = 0, 'Ovqat'
        MENU = 1, 'Menu'
        RECIPE = 2, 'Retsept'

    # === Unique identifier for the food order. ===
    food_order_id = models.CharField(default=new_id, max_length=24, unique=True)
    # === Reference to the food item being ordered. ===
    food = models.ForeignKey('foods.Food', on_delete=models.PROTECT, related_name='food_orders', blank=True, null=True)
    # === Reference to the menu being ordered. ===
    menu = models.ForeignKey('menus.Menu', on_delete=models.PROTECT, related_name='food_orders', blank=True, null=True)
    # === Reference to the recipe being ordered. ===
    recipe = models.ForeignKey('menus.Recipe', on_delete=models.PROTECT, related_name='food_orders', blank=True,
                               null=True)
    # === Reference to the counter agent being ordered. ===
    counter_agent = models.ForeignKey('counter_agents.CounterAgent', on_delete=models.PROTECT,
                                      related_name='food_orders')
    # === Reference to the hotel associated with the order. ===
    hotel_order = models.ForeignKey('orders.HotelOrder', on_delete=models.PROTECT, related_name='food_orders',
                                    blank=True, null=True)

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

    @property
    def total_price(self):
        return self.price * self.product_count

    def clean(self):
        if bool(self.food) + bool(self.menu) + bool(self.recipe) != 1:
            raise CustomExceptionError(detail="Input 1 type of product")

            # Agar faqat `food` tanlangan bo‘lsa, `product_type` FOOD bo‘lishi kerak
        if self.food and self.product_type != FoodOrder.ProductType.FOOD:
            raise CustomExceptionError(detail="If food is selected, product_type must be FOOD (0).")

            # Agar `menu` tanlangan bo‘lsa, `product_type` MENU bo‘lishi kerak
        if self.menu and self.product_type != FoodOrder.ProductType.MENU:
            raise CustomExceptionError(detail="If menu is selected, product_type must be MENU (1).")

            # Agar `recipe` tanlangan bo‘lsa, `product_type` RECIPE bo‘lishi kerak
        if self.recipe and self.product_type != FoodOrder.ProductType.RECIPE:
            raise CustomExceptionError(detail="If recipe is selected, product_type must be RECIPE (2).")

            # Agar `food` bo‘lsa, order_type faqat ONCE bo‘lishi kerak
        if self.food and self.order_type != FoodOrder.OrderType.ONCE:
            raise CustomExceptionError(detail="Food orders must be one-time (ONCE).")

            # Agar `menu` yoki `recipe` bo‘lsa, order_type faqat CONTINUOUS bo‘lishi kerak
        if (self.menu or self.recipe) and self.order_type != FoodOrder.OrderType.CONTINUOUS:
            raise CustomExceptionError(detail="Menu and Recipe orders must be continuous (CONTINUOUS).")

    def save(self, *args, **kwargs):
        if self.product_type in [FoodOrder.ProductType.MENU, FoodOrder.ProductType.RECIPE]:
            self.order_type = FoodOrder.OrderType.CONTINUOUS

        elif self.product_type == FoodOrder.ProductType.FOOD:
            self.order_type = FoodOrder.OrderType.ONCE

        elif (
            self.product_type in [FoodOrder.ProductType.MENU, FoodOrder.ProductType.RECIPE]
            and self.order_type != FoodOrder.OrderType.CONTINUOUS
        ):
            raise CustomExceptionError(code=400, detail="An order for a menu or recipe should only be a standing order.")

        elif (
            self.product_type == FoodOrder.ProductType.FOOD
            and self.order_type != FoodOrder.OrderType.ONCE
        ):
            raise CustomExceptionError(code=400, detail="The order for food should only be one-time.")

        super().save(*args, **kwargs)