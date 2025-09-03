from decimal import ROUND_UP, Decimal
from django.db import models
from django.db.models import F, When, Value, FloatField, Case, ExpressionWrapper, Sum
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
    count = models.FloatField(validators=[MinValueValidator(1)])
    # === Price of the product item, stored as a floating-point number. Must be ≥ 0. ===
    price = models.FloatField(default=0, validators=[MinValueValidator(0)])
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
        warehouse = warehouse.annotate(
            exact_quantity=F("count")
            * Case(
                When(product__difference_measures=0, then=Value(1)),
                default=F("product__difference_measures"),
                output_field=FloatField(),
            ),
            net_price=ExpressionWrapper(
                F("gross_price")
                / Case(
                    When(
                        product__difference_measures__isnull=False,
                        then=F("arrived_count") * Case(
                            When(product__difference_measures=0, then=Value(1)),
                            default=F("product__difference_measures"),
                            output_field=FloatField()
                        ),
                    ),
                    default=F("arrived_count"),
                    output_field=FloatField(),
                ),
                output_field=FloatField(),
            ),
        )

        price_obj = (
            warehouse.filter(exact_quantity__gte=self.count)
            .order_by("created_at")
            .first()
            or warehouse.order_by("-created_at").first()
        )
        return float(price_obj.get_net_price()) if price_obj else float(self.price or 0)

    def calculate_prices(self, warehouse=None):
        if warehouse is None:
            warehouse, _ = self.get_product_in_warehouse()

        net_price = self.calculate_net_price(warehouse)
        self.price = Decimal(net_price * self.count).quantize(
            Decimal("0.0001"), rounding=ROUND_UP
        )

    def save(self, *args, **kwargs):
        warehouse, product = self.get_product_in_warehouse()
        self.calculate_prices(warehouse=warehouse)
        product_count = warehouse.aggregate(total=Sum("count"))["total"] or 0

        if (
            product_count == 0
            or self.count > product_count * product.difference_measures
        ):
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
