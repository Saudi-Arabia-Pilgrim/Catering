from django.db import models

from apps.base.models import AbstractBaseModel


class Recipe(AbstractBaseModel):
    """
    Recipe model representing a recipe associated with different menus (breakfast, lunch, dinner).
    """
    # === Foreign key to the Menu model for breakfast recipes. ===
    menu_breakfast = models.ForeignKey(
        "menus.Menu",
        on_delete=models.PROTECT,
        related_name="breakfast_recipes",
    )
    # === Foreign key to the Menu model for lunch recipes. ===
    menu_lunch = models.ForeignKey(
        "menus.Menu",
        on_delete=models.PROTECT,
        related_name="lunch_recipes",
    )
    # === Foreign key to the Menu model for dinner recipes. ===
    menu_dinner = models.ForeignKey(
        "menus.Menu",
        on_delete=models.PROTECT,
        related_name="dinner_recipes",
    )
    # === Name of the recipe. ===
    name = models.CharField(max_length=255)
    # === Unique slug for the recipe. ===
    slug = models.SlugField(max_length=255, unique=True)
    # === Number of products in the recipe. ===
    count_of_products = models.FloatField()
    # === Status of the recipe, default is True (active). ===
    status = models.BooleanField(default=True)
    # === Price of the recipe, with a maximum of 10 digits and 2 decimal places. ===
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    class Meta:
        # === The database table name for the model. ===
        db_table = 'recipe'
        # === The singular name for the model in the admin interface. ===
        verbose_name = 'Recipe'
        # === The plural name for the model in the admin interface. ===
        verbose_name_plural = 'Recipes'

    def __str__(self):
        """
        Returns a string representation of the recipe, including its name, count of products, and price.
        """
        return f"{self.name} - {self.count_of_products} - {self.price}"