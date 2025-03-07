from django.db import models

from apps.base.models import AbstractBaseModel


class Food(AbstractBaseModel):
    """
    Food model representing a food item in the catering application.

    Attributes:
        recipe (ForeignKey): Foreign key to the RecipeFood model, with a protect delete rule.
        name (CharField): Name of the food item, with a maximum length of 255 characters.
        slug (SlugField): Unique slug for the food item, with a maximum length of 255 characters.
        status (BooleanField): Status of the food item, default is True.
        net_price (DecimalField): Net price of the food item, with a maximum of 10 digits and 2 decimal places.
        image (ImageField): Optional image of the food item, uploaded to 'foods/%Y/%m/%d/'.
        section (PositiveSmallIntegerField): Section of the food item, chosen from predefined choices (LIQUID or DEEP).

    Meta:
        db_table (str): Name of the database table.
        verbose_name (str): Human-readable name of the model.
        verbose_name_plural (str): Human-readable plural name of the model.

    Methods:
        __str__(): Returns the name of the food item.
    """
    class Section(models.IntegerChoices):
        LIQUID = 0, 'Suyuq'
        DEEP = 1, 'Quyuq'

    # === Foreign key to the RecipeFood model, with a protect delete rule. ===
    recipe = models.ForeignKey('foods.RecipeFood', on_delete=models.PROTECT, related_name='foods')
    # === Name of the food item, with a maximum length of 255 characters. ===
    name = models.CharField(max_length=255)
    # === Unique slug for the food item, with a maximum length of 255 characters. ===
    slug = models.SlugField(max_length=255, unique=True)
    # === Status of the food item, default is True. ===
    status = models.BooleanField(default=True)
    # === Net price of the food item, with a maximum of 10 digits and 2 decimal places. ===
    net_price = models.DecimalField(max_digits=10, decimal_places=2)
    # === Optional image of the food item, uploaded to 'foods/%Y/%m/%d/'. ===
    image = models.ImageField(upload_to='foods/%Y/%m/%d/', null=True, blank=True)
    # === Section of the food item, chosen from predefined choices (LIQUID or DEEP). ===
    section = models.PositiveSmallIntegerField(choices=Section.choices)

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