from decimal import ROUND_UP, Decimal
from django.db import models
from django.db.models import Q, OuterRef, Exists, Sum, DecimalField
from django.core.validators import MinValueValidator
from django.utils.text import slugify

from apps.base.exceptions import CustomExceptionError
from apps.menus.models.recipe import Recipe
from apps.base.models import AbstractBaseModel


class Menu(AbstractBaseModel):
    """
    A menu model representing a menu (breakfast, lunch or dinner) in a catering application.
    """

    # translation_fields = ["name"]

    # === The name of the menu. ===
    name = models.CharField(max_length=255)
    # === A unique slug for the menu. ===
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    # === A many-to-many relationship with the Food model. ===
    foods = models.ManyToManyField("foods.Food", related_name="menus")
    # === The status of the menu, default is True. ===
    status = models.BooleanField(default=True)
    # === An optional image for the menu, uploaded to 'menus/%Y/%m/%d/'. ===
    image = models.ImageField(upload_to="menus/%Y/%m/%d/", blank=True, null=True)

    # === The net price of the menu, optional. ===
    net_price = models.FloatField(default=0, blank=True)
    # === The profit associated with the menu. ===
    profit = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(1)]
    )
    # === Menu price considering profit. ===
    gross_price = models.FloatField(default=0, blank=True)

    class Meta:
        # === The database table name for the model. ===
        db_table = "menu"
        # === The singular name for the model in the admin interface. ===
        verbose_name = "Menu"
        # === The plural name for the model in the admin interface. ===
        verbose_name_plural = "Menus"
        # === Ordering field for sorting a set of queries ===
        ordering = ["-created_at"]

    def __str__(self):
        """
        Returns a string representation of the menu, including its name, gross price, and count of products.
        """
        return f"{self.name} - {self.gross_price}"

    def get_foods(self):
        return self.foods.only("net_price", "status")

    def calculate_prices(self, foods=None):
        if foods is None:
            foods = self.foods.all()

        has_zero_price = any(food.net_price == 0 for food in foods)

        if has_zero_price:
            net_price = Decimal(0)
        else:
            net_price = foods.aggregate(
                total=Sum("net_price", output_field=DecimalField())
            )["total"] or Decimal(0)

        self.net_price = net_price.quantize(Decimal("0.0001"), rounding=ROUND_UP)
        self.gross_price = (
            (self.net_price + self.profit).quantize(
                Decimal("0.0001"), rounding=ROUND_UP
            )
            if net_price > 0
            else 0
        )

    def change_status(self, foods=None):
        if foods is None:
            foods = self.get_foods()
        self.status = all(food.status for food in foods)

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        obj = self.__class__.objects.filter(slug=slug).exclude(pk=self.pk).first()
        if obj:
            raise CustomExceptionError(
                code=400, detail="A menu with this name already exists"
            )
        self.slug = slug
        super().save(*args, **kwargs)

    def changing_dependent_objects(self):
        recipes = Recipe.objects.annotate(
            has_inactive_menu=Exists(
                Menu.objects.filter(
                    Q(pk=OuterRef("menu_breakfast_id"))
                    | Q(pk=OuterRef("menu_lunch_id"))
                    | Q(pk=OuterRef("menu_dinner_id")),
                    status=False,
                )
            )
        )

        for recipe in recipes:
            recipe.status = not recipe.has_inactive_menu
            recipe.calculate_prices()

        Recipe.objects.bulk_update(recipes, ["status", "net_price", "gross_price"])

    def change_dependent(self):
        self.change_object()
        self.save()
        self.changing_dependent_objects()

    def change_object(self):
        foods = self.get_foods()
        self.change_status(foods)
        self.calculate_prices(foods)
