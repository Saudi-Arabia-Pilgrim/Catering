from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify

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
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    # === Number of products in the recipe. ===
    count_of_products = models.PositiveSmallIntegerField()
    # === Status of the recipe, default is True (active). ===
    status = models.BooleanField(default=True)
    # === Net price of the recipe. ===
    net_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, validators=[MinValueValidator(1)])
    # === Profit associated with the recipe. ===
    profit = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    # === Gross price of the recipe. ===
    gross_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, validators=[MinValueValidator(1)])

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
        return f"{self.name} - {self.count_of_products} - {self.gross_price}"

    def clean(self):
        """
        Clean method for the Recipe model.

        This method performs additional operations before saving the instance:
        1. Generates a slug from the recipe name if it doesn't exist or doesn't match the current slug.
        2. Calculates the total count of products from associated breakfast, lunch, and dinner menus.
        3. Calculates the net price from associated menus.
        4. Calculates the gross price by adding profit to net price.
        5. Updates status based on associated menus.
        """
        self.slug = slugify(self.name)

        menus = [self.menu_breakfast, self.menu_lunch, self.menu_dinner]

        self.count_of_products = sum(menu.count_of_products for menu in menus)
        self.net_price = sum(menu.net_price for menu in menus)

        self.gross_price = self.net_price + self.profit

        self.status = all(menu.status for menu in menus)