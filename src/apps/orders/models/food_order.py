from collections import defaultdict
from datetime import timedelta
from decimal import ROUND_UP, Decimal

from django.utils.timezone import now
from django.db import models, transaction
from django.db.models import Sum, F, Q, Prefetch, Case, When, FloatField, Value

from apps.orders.utils import new_id
from apps.base.exceptions import CustomExceptionError
from apps.base.models import AbstractBaseModel
from apps.menus.models import Menu
from apps.products.models import Product
from apps.warehouses.models import Warehouse
from apps.foods.models import Food
from apps.warehouses.utils.update_product_dependencies import update_product_dependencies_in_warehouse


class FoodOrder(AbstractBaseModel):
    """
    Model representing a food order.
    """

    class OrderType(models.IntegerChoices):
        CONTINUOUS = 0, "Davomiy"
        ONCE = 1, "Bir martalik"

    class ProductType(models.IntegerChoices):
        FOOD = 0, "Ovqat"
        MENU = 1, "Menu"
        RECIPE = 2, "Retsept"

    # === Unique identifier for the food order. ===
    food_order_id = models.CharField(default=new_id, max_length=24, unique=True)
    # === Reference to the food item being ordered. ===
    food = models.ForeignKey(
        "foods.Food",
        on_delete=models.PROTECT,
        related_name="orders",
        blank=True,
        null=True,
    )
    # === Reference to the menu being ordered. ===
    menu = models.ForeignKey(
        "menus.Menu",
        on_delete=models.PROTECT,
        related_name="orders",
        blank=True,
        null=True,
    )
    # === Reference to the recipe being ordered. ===
    recipe = models.ForeignKey(
        "menus.Recipe",
        on_delete=models.PROTECT,
        related_name="orders",
        blank=True,
        null=True,
    )
    # === Reference to the counter agent being ordered. ===
    counter_agent = models.ForeignKey(
        "counter_agents.CounterAgent",
        on_delete=models.PROTECT,
        related_name="orders",
        limit_choices_to={"status": True}
    )

    # === The time when the order was placed. ===
    order_time = models.DateField(blank=True, null=True)

    # === The type of order (continuous or once). ===
    order_type = models.PositiveSmallIntegerField(choices=OrderType.choices, blank=True)
    # === The type of product (food, menu, or recipe). ===
    product_type = models.PositiveSmallIntegerField(
        choices=ProductType.choices, blank=True
    )

    # === The price of the order. ===
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # ===  The address where the order should be delivered. ===
    address = models.CharField(max_length=1200, blank=True, null=True)

    # === The number of products in the order. ===
    product_count = models.PositiveSmallIntegerField(default=1)

    # === Status of the order item, default is False. ===
    status = models.BooleanField(default=False)

    class Meta:
        # === The name of the database table. ===
        db_table = "food_order"
        # === The human-readable name of the model. ===
        verbose_name = "Food order"
        # === The human-readable plural name of the model. ===
        verbose_name_plural = "Food orders"

    def __str__(self):
        """
        Returns a string representation of the food order.
        """
        return f"{self.food_order_id} - {self.get_order_type_display()} - {self.price}"

    @property
    def profit(self):
        products = {
            self.ProductType.FOOD: "food",
            self.ProductType.MENU: "menu",
            self.ProductType.RECIPE: "recipe",
        }
        product = getattr(self, products[self.product_type])
        return product.profit

    @property
    def total_price(self):
        return Decimal(self.price * self.product_count).quantize(
                Decimal("0.001"), rounding=ROUND_UP
            )

    @property
    def experience_date_str(self):
        if not self.order_time:
            return None
        experience_date = self.order_time + timedelta(days=7)
        return f"{experience_date.day}.{experience_date.month}.{experience_date.year}"
    
    @property
    def experience_date(self):
        if not self.order_time:
            return None
        return self.order_time + timedelta(days=7)
    
    def order_ready(self):
        if self.order_time and self.experience_date > now().date():
            raise CustomExceptionError(code=400, detail="The order cannot be marked as ready yet.")
        self.__class__.objects.filter(id=self.id).update(status=True)

    def save(self, *args, **kwargs):
        self.validate_products()
        self.selected_product_type()
        self.selected_order_type()
        self.validate_order_type()
        self.validate_order_time()
        self.set_price()
        self.deduction_of_goods_from_the_warehouse()
        super().save(*args, **kwargs)

    def selected_product_type(self):
        self.product_type = (
            self.ProductType.FOOD
            if self.food
            else self.ProductType.MENU if self.menu else self.ProductType.RECIPE
        )

    def validate_order_time(self):
        if self.order_time and self.order_time < now().date():
            raise CustomExceptionError(
                code=400, detail="Order time cannot be in the past."
            )

    def validate_products(self):
        if bool(self.food) + bool(self.menu) + bool(self.recipe) != 1:
            raise CustomExceptionError(detail="Input 1 type of product")

    def validate_order_type(self):
        if self.order_type == self.OrderType.CONTINUOUS and not self.order_time:
            raise CustomExceptionError(
                code=400, detail="Order time must be specified for continuous orders."
            )
        if self.order_type == self.OrderType.ONCE and self.order_time:
            self.order_time = None

    def selected_order_type(self):
        if self.product_type in [
            self.ProductType.MENU,
            self.ProductType.RECIPE,
        ]:
            self.order_type = self.OrderType.CONTINUOUS

        else:
            self.order_type = self.OrderType.ONCE

    def set_price(self):
        match self.product_type:
            case self.ProductType.FOOD:
                self.price = self.food.gross_price
            case self.ProductType.MENU:
                self.price = self.menu.gross_price
            case self.ProductType.RECIPE:
                self.price = self.recipe.gross_price

    def process_product_deductions(self, products_needed: dict):
        product_ids = [product_id for product_id, need in products_needed.items()]
        products_dict = Product.objects.in_bulk(product_ids)
        warehouses = (
            Warehouse.objects.select_related("product", "product__measure")
            .filter(Q(status=True) & Q(product_id__in=product_ids))
            .select_for_update()
        )
        food_shortages = {}

        for product_id, required_quantity in products_needed.items():
            product = products_dict[product_id]

            total_available = (
                warehouses.filter(product_id=product_id).aggregate(
                    total=Sum(
                        F("count")
                        * Case(
                            When(product__difference_measures=0, then=Value(1)),
                            default=F("product__difference_measures"),
                            output_field=FloatField(),
                        )
                    )
                )["total"]
                or 0
            )

            if total_available < required_quantity:
                if product_id not in food_shortages:
                    food_shortages[str(product_id)] = {
                        "name": product.name,
                        "needed": (required_quantity - total_available),
                        "measure": product.measure.abbreviation,
                    }
                else:
                    food_shortages[str(product_id)]["needed"] += (
                        required_quantity - total_available
                    )

        if food_shortages:
            raise CustomExceptionError(code=400, detail=food_shortages)

        update_warehouses = []

        for product_id, required_quantity in products_needed.items():
            product = products_dict[product_id]
            product_warehouses = warehouses.filter(product_id=product_id).order_by(
                "created_at"
            )

            for warehouse_item in product_warehouses:
                available_quantity = (
                    warehouse_item.count * product.difference_measures
                    if product.difference_measures
                    else 1
                )
                if available_quantity >= required_quantity:
                    warehouse_item.count -= (
                        required_quantity / product.difference_measures
                    )
                    if warehouse_item.count == 0:
                        warehouse_item.status = False
                    update_warehouses.append(warehouse_item)
                    break
                else:
                    required_quantity -= available_quantity
                    warehouse_item.count = 0
                    warehouse_item.status = False
                    update_warehouses.append(warehouse_item)

        Warehouse.objects.bulk_update(update_warehouses, ["status", "count"])

        update_product_dependencies_in_warehouse(product_ids)

    def deduction_of_goods_from_the_warehouse(self):
        with transaction.atomic():
            products_needed = defaultdict(int)
            match self.product_type:
                case self.ProductType.FOOD:
                    recipe_foods = self.food.recipes.all()
                    for recipe in recipe_foods:
                        products_needed[recipe.product_id] += (
                            recipe.count * self.product_count
                        )
                case self.ProductType.MENU:
                    foods = self.menu.foods.all().prefetch_related("recipes")

                    for food in foods:
                        for recipe in food.recipes.all():
                            products_needed[recipe.product_id] += (
                                recipe.count * self.product_count
                            )

                case self.ProductType.RECIPE:
                    menus = Menu.objects.filter(
                        Q(breakfast_recipes=self.recipe)
                        | Q(lunch_recipes=self.recipe)
                        | Q(dinner_recipes=self.recipe)
                    ).prefetch_related(
                        Prefetch(
                            "foods", queryset=Food.objects.prefetch_related("recipes")
                        )
                    )

                    for menu in menus:
                        for food in menu.foods.all():
                            for recipe in food.recipes.all():
                                products_needed[recipe.product_id] += (
                                    recipe.count * self.product_count
                                )

            self.process_product_deductions(products_needed)
