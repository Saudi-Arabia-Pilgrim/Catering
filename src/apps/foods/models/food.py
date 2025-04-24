from decimal import ROUND_UP, Decimal
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator

from apps.base.exceptions.exception_error import CustomExceptionError
from apps.base.models import AbstractBaseModel
from apps.foods.utils import CalculatePrices
from apps.menus.models import Menu


class Food(AbstractBaseModel):
    """
    Food model representing a food item in the catering application.
    """

    class Section(models.IntegerChoices):
        LIQUID = 0, "Suyuq"
        DEEP = 1, "Quyuq"

    # === Name of the food item, with a maximum length of 255 characters. ===
    name = models.CharField(max_length=255)
    # === Unique slug for the food item, with a maximum length of 255 characters. ===
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    # === Foreign key to the RecipeFood model, with a protect delete rule. ===
    recipes = models.ManyToManyField("foods.RecipeFood", related_name="foods")
    # === Section of the food item, chosen from predefined choices (LIQUID or DEEP). ===
    section = models.PositiveSmallIntegerField(choices=Section.choices)
    # === Status of the food item, default is True. ===
    status = models.BooleanField(default=True)

    # === Net price of the food item, with a maximum of 10 digits and 2 decimal places. ===
    net_price = models.FloatField(default=0)
    # === Profit associated with the food item. ===
    profit = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(1)]
    )
    # === Gross price of the food item, calculated as the sum of the net price and profit. ===
    gross_price = models.FloatField(default=0)

    # === Optional image of the food item, uploaded to 'foods/%Y/%m/%d/'. ===
    image = models.ImageField(upload_to="foods/%Y/%m/%d/", null=True, blank=True)

    class Meta:
        # === Name of the database table. ===
        db_table = "food"
        # === Human-readable name of the model. ===
        verbose_name = "Food"
        # === Human-readable plural name of the model. ===
        verbose_name_plural = "Foods"

    def __str__(self):
        """
        Returns the name of the food item.
        """
        return self.name

    def get_food_recipes(self):
        return self.recipes.only("price", "status")

    def calculate_prices(self, recipes=None):
        if recipes is None:
            recipes = self.recipes.all()

        has_zero_price = False

        for recipe in recipes:
            if recipe.price == 0:
                has_zero_price = True
                break

        if has_zero_price:
            net_price = Decimal(0)
        else:
            net_price = sum([Decimal(recipe.price) or Decimal(0) for recipe in recipes], Decimal(0))

        self.net_price = net_price.quantize(Decimal("0.0001"), rounding=ROUND_UP)
        self.gross_price = (
            (self.net_price + self.profit).quantize(
                Decimal("0.0001"), rounding=ROUND_UP
            )
            if net_price > 0
            else 0
        )

    def check_status(self, recipes=None):
        if recipes is None:
            self.status = not self.recipes.filter(status=False).exists()
        else:
            self.status = all([recipe.status for recipe in recipes])

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        obj = self.__class__.objects.filter(slug=slug).exclude(pk=self.pk).exists()
        if obj:
            raise CustomExceptionError(
                code=400, detail="A food with this name already exists"
            )
        self.slug = slug
        super().save(*args, **kwargs)

    def changing_dependent_objects(self):
        menus = self.menus.annotate(
            has_inactive_food=models.Exists(self.menus.filter(foods__status=False))
        )

        for menu in menus:
            menu.status = not menu.has_inactive_food
            menu.calculate_prices()

        Menu.objects.bulk_update(menus, ["net_price", "gross_price", "status"])
        CalculatePrices.calculate_objects(objs=menus, type="food")

    def change_dependent(self):
        self.change_object()
        self.save()
        self.changing_dependent_objects()

    def change_object(self):
        recipes = self.get_food_recipes()
        self.check_status(recipes)
        self.calculate_prices(recipes)

    def delete(self, using=None, keep_parents=False):
        if self.menus.exists():
            raise CustomExceptionError(
                code=423,
                detail="This object cannot be deleted because it is referenced by other objects.",
            )
        return super().delete(using, keep_parents)
