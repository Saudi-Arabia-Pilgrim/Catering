from django.db import models

from apps.base.models import AbstractBaseModel


class RecipeFood(AbstractBaseModel):
    """
    RecipeFood model represents the relationship between a product and its usage in a recipe.
    """
    # === A foreign key to the Product model, representing the product used in the recipe. ===
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='recipe_foods')
    # === The quantity of the product used in the recipe. ===
    count = models.FloatField()

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
        return f'{self.count} - {self.price}'