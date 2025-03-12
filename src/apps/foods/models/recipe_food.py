from django.db import models
from django.core.validators import MinValueValidator

from apps.base.models import AbstractBaseModel
from apps.warehouses.models import Warehouse


class RecipeFood(AbstractBaseModel):
    """
    RecipeFood model represents the relationship between a product and its usage in a recipe.
    """
    # === A foreign key to the Product model, representing the product used in the recipe. ===
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='recipe_foods')
    # === The quantity of the product used in the recipe. ===
    count = models.FloatField(validators=[MinValueValidator(1)])
    # === Price of the product item, with a maximum of 10 digits and 2 decimal places. ===
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
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

    def clean(self):
        warehouse = Warehouse.objects.filter(product=self.product)

        product_count = warehouse.aggregate(total=models.Sum('count'))['total'] or 0
        if product_count == 0 or self.count > product_count:
            self.status = False

        price_obj = warehouse.filter(count__gte=self.count).order_by('net_price').first() or \
                    warehouse.order_by('net_price').last()
        self.price = price_obj.net_price if price_obj else self.price or 0
