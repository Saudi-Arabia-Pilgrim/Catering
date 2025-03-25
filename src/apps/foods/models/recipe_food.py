from decimal import ROUND_DOWN, Decimal
from django.db import models
from django.core.validators import MinValueValidator

from apps.base.models import AbstractBaseModel
from apps.foods.models.food import Food
from apps.warehouses.models import Warehouse


class RecipeFood(AbstractBaseModel):
    """
    RecipeFood model represents the relationship between a product and its usage in a recipe.
    """
    # === A foreign key to the Product model, representing the product used in the recipe. ===
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='recipe_foods')
    # === The quantity of the product used in the recipe. ===
    count = models.FloatField(validators=[MinValueValidator(1)])
    # === Price of the product item, stored as a floating-point number. Must be ≥ 0. ===
    price = models.FloatField(default=0, validators=[MinValueValidator(0)])
    # === Status of the recipe food item. ===
    status = models.BooleanField(default=True)

    class Meta:
        # === The name of the database table. ===
        db_table = 'recipe_food'
        # === The human-readable name of the model. ===
        verbose_name = 'Recipe Food'
        # === The human-readable plural name of the model. ===
        verbose_name_plural = 'Recipe Foods'

    def __str__(self):
        """
        Returns a string representation of the RecipeFood instance.
        """
        return f'{self.product.name} - {self.count} - {self.price}'
    
    def get_product_in_warehouse(self):
        product = self.product
        return Warehouse.objects.filter(product=product), product

    def calculate_net_price(self, warehouse):
        warehouse = warehouse.annotate(
            net_price=models.ExpressionWrapper(
                models.F("gross_price") / models.Case(
                    models.When(product__difference_measures__isnull=False, then=models.F("arrived_count") * models.F("product__difference_measures")),
                    default=models.F("arrived_count"),
                    output_field=models.DecimalField()
                ),
                output_field=models.DecimalField()
            )
        )

        price_obj = warehouse.filter(count__gte=self.count).order_by("net_price").first() or \
                    warehouse.order_by("-net_price").first()
        return float(price_obj.get_net_price()) if price_obj else float(self.price or 0)
    
    def calculate_prices(self, warehouse=None):
        if warehouse is None:
            warehouse, _ = self.get_product_in_warehouse()

        net_price = self.calculate_net_price(warehouse)
        self.price = Decimal(net_price * self.count).quantize(Decimal("0.0001"), rounding=ROUND_DOWN)

    def save(self, *args, **kwargs):
        warehouse, product = self.get_product_in_warehouse()
        self.calculate_prices(warehouse=warehouse)
        product_count = warehouse.aggregate(total=models.Sum("count"))['total'] or 0

        if product_count == 0 or self.count > product_count * product.difference_product:
            self.status = False
        else:
            self.status = True

        super().save(*args, **kwargs)
        self.changing_dependent_objects()

    def changing_dependent_objects(self):
        foods = self.foods.all().prefetch_related("recipes")
        for food in foods:
            food.calculate_prices()
        Food.objects.bulk_update(foods, ["net_price", "gross_price"])
        for food in foods:
            food.changing_dependent_objects()