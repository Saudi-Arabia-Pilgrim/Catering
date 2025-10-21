from decimal import ROUND_UP, ROUND_HALF_UP, Decimal
from django.db import models
from django.db.models import F, When, Value, DecimalField, Case, ExpressionWrapper, Sum
from django.core.validators import MinValueValidator

from apps.base.exceptions import CustomExceptionError
from apps.base.models import AbstractBaseModel
from apps.foods.models.food import Food
from apps.foods.utils import CalculatePrices
from apps.warehouses.models import Warehouse


class RecipeFood(AbstractBaseModel):
    """
    RecipeFood model represents the relationship between a product and its usage in a recipe.
    """

    # === A foreign key to the Product model, representing the product used in the recipe. ===
    product = models.ForeignKey(
        "products.Product", on_delete=models.PROTECT, related_name="recipe_foods"
    )
    # === The quantity of the product used in the recipe. ===
    count = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    # === Price of the product item. Must be ≥ 0. ===
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    # === Status of the recipe food item. ===
    status = models.BooleanField(default=True)

    class Meta:
        # === The name of the database table. ===
        db_table = "recipe_food"
        # === The human-readable name of the model. ===
        verbose_name = "Recipe Food"
        # === The human-readable plural name of the model. ===
        verbose_name_plural = "Recipe Foods"
        # === Ordering field for sorting a set of queries ===
        ordering = ["-created_at"]

    def __str__(self):
        """
        Returns a string representation of the RecipeFood instance.
        """
        return f"{self.count} - {self.price}"

    def get_product_in_warehouse(self):
        product = self.product
        return (
            Warehouse.objects.filter(product=product).select_related("product"),
            product,
        )

    def calculate_net_price(self, warehouse):
        """
        Calculate net price for the recipe food item.
        Returns Decimal value rounded to 2 decimal places.
        """
        warehouse = warehouse.annotate(
            exact_quantity=F("count")
            * Case(
                When(product__difference_measures=0, then=Value(1)),
                default=F("product__difference_measures"),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
            net_price=ExpressionWrapper(
                F("gross_price")
                / Case(
                    When(
                        product__difference_measures__isnull=False,
                        then=F("arrived_count") * Case(
                            When(product__difference_measures=0, then=Value(1)),
                            default=F("product__difference_measures"),
                            output_field=DecimalField(max_digits=10, decimal_places=2)
                        ),
                    ),
                    default=F("arrived_count"),
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                ),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
        )

        price_obj = (
            warehouse.filter(exact_quantity__gte=self.count)
            .order_by("created_at")
            .first()
            or warehouse.order_by("-created_at").first()
        )
        if price_obj:
            result = price_obj.get_net_price()
            return Decimal(str(result)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return Decimal(str(self.price or 0)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def calculate_prices(self, warehouse=None):
        """
        Calculate prices for the recipe food item.
        Prices are rounded to 2 decimal places using ROUND_HALF_UP.
        """
        if warehouse is None:
            warehouse, _ = self.get_product_in_warehouse()

        net_price = self.calculate_net_price(warehouse)
        self.price = (Decimal(str(net_price)) * self.count).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    def save(self, *args, **kwargs):
        warehouse, product = self.get_product_in_warehouse()
        self.calculate_prices(warehouse=warehouse)
        product_count = warehouse.aggregate(total=Sum("count"))["total"] or Decimal('0')

        # Calculate actual available quantity considering difference_measures
        difference_measures = product.difference_measures if product.difference_measures else Decimal('1')
        available_quantity = product_count * difference_measures

        if product_count == Decimal('0') or self.count > available_quantity:
            self.status = False
        else:
            self.status = True

        super().save(*args, **kwargs)
        self.changing_dependent_objects()

    def changing_dependent_objects(self):
        foods = list(self.foods.all().prefetch_related("recipes").distinct())
        for food in foods:
            food.calculate_prices()
        Food.objects.bulk_update(foods, ["net_price", "gross_price"])
        CalculatePrices.calculate_objects(objs=foods, type="recipe_food")

    def delete(self, using=None, keep_parents=False):
        if self.foods.exists():
            raise CustomExceptionError(
                code=423,
                detail="This object cannot be deleted because it is referenced by other objects.",
            )
        return super().delete(using=None, keep_parents=False)
