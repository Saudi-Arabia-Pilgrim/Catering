from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator

from apps.base.models import AbstractBaseModel


class Food(AbstractBaseModel):
    """
    Food model representing a food item in the catering application.
    """

    class Section(models.IntegerChoices):
        LIQUID = 0, 'Suyuq'
        DEEP = 1, 'Quyuq'

    # === Name of the food item, with a maximum length of 255 characters. ===
    name = models.CharField(max_length=255)
    # === Unique slug for the food item, with a maximum length of 255 characters. ===
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    # === Foreign key to the RecipeFood model, with a protect delete rule. ===
    recipes = models.ManyToManyField('foods.RecipeFood', related_name='foods')
    # === Section of the food item, chosen from predefined choices (LIQUID or DEEP). ===
    section = models.PositiveSmallIntegerField(choices=Section.choices)
    # === Status of the food item, default is True. ===
    status = models.BooleanField(default=True)
    
    # === Net price of the food item, with a maximum of 10 digits and 2 decimal places. ===
    net_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    # === Profit associated with the food item. ===
    profit = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    # === Gross price of the food item, calculated as the sum of the net price and profit. ===
    gross_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    
    # === Optional image of the food item, uploaded to 'foods/%Y/%m/%d/'. ===
    image = models.ImageField(upload_to='foods/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        # === Name of the database table. ===
        db_table = 'food'
        # === Human-readable name of the model. ===
        verbose_name = 'Food'
        # === Human-readable plural name of the model. ===
        verbose_name_plural = 'Foods'

    def __str__(self):
        """
        Returns the name of the food item.
        """
        return self.name

    def get_net_price(self):
        """
        Calculate the net price of the food item based on its recipes.

        This method iterates over all the recipes associated with the food item,
        sums up their prices, and returns the total price along with a flag indicating
        whether the product exists.

        Returns:
            tuple: A tuple containing:
                - float: The total price of all recipes if the product exists, otherwise 0.
                - bool: A flag indicating whether the product exists (False if any recipe has a price of 0).
        """
        if self.recipes.filter(price=0).exists():
            return 0, False

        total_price = self.recipes.aggregate(total=models.Sum('price'))['total'] or 0
        return total_price, True if total_price != 0 else False

    def clean(self):
        """
        Override the clean method to perform additional operations before saving the model instance.
        This method performs the following operations:
        1. Sets the slug field based on the name field if it is not already set or if it does not match the slug.
        2. Calculates the net price and checks if the product exists.
        3. Sets the status to False if the product does not exist.
        4. Calculates the gross price by adding the profit to the net price.
        5. Calls the superclass's save method to save the instance.
        """
        self.slug = slugify(self.name)

        self.net_price, self.status = self.get_net_price()

        self.gross_price = self.net_price + self.profit if self.net_price else 0
