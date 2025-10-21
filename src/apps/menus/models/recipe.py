from decimal import ROUND_UP, ROUND_HALF_UP, Decimal

from django.db import models
from django.db.models import DecimalField, Q, F, OuterRef, Exists, Value
from django.db.models.functions import Coalesce
from django.core.validators import MinValueValidator
from django.utils.text import slugify

from apps.base.exceptions import CustomExceptionError
from apps.base.models import AbstractBaseModel


class Recipe(AbstractBaseModel):
    """
    Recipe model representing a recipe associated with different menus (breakfast, lunch, dinner).
    """

    # translation_fields = ["name"]

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
    # === Status of the recipe, default is True (active). ===
    status = models.BooleanField(default=True)
    # === Net price of the recipe. ===
    net_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    # === Profit associated with the recipe. ===
    profit = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(1)]
    )
    # === Gross price of the recipe. ===
    gross_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)

    class Meta:
        # === The database table name for the model. ===
        db_table = "recipe"
        # === The singular name for the model in the admin interface. ===
        verbose_name = "Recipe"
        # === The plural name for the model in the admin interface. ===
        verbose_name_plural = "Recipes"
        # === Ordering field for sorting a set of queries ===
        ordering = ["-created_at"]

    def __str__(self):
        """
        Returns a string representation of the recipe, including its name, count of products, and price.
        """
        return f"{self.name} - {self.gross_price}"

    def get_menus(self):
        menus_id = [self.menu_breakfast_id, self.menu_lunch_id, self.menu_dinner_id]
        return list(self.menu_breakfast.__class__.objects.filter(id__in=menus_id))

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        obj = self.__class__.objects.filter(slug=slug).exclude(pk=self.pk).first()
        if obj:
            raise CustomExceptionError(
                code=400, detail="A recipe with this name already exists"
            )
        self.slug = slug

        menus = self.get_menus()

        self.calculate_prices(menus=menus)
        self.status = all(menu.status for menu in menus)

        super().save(*args, **kwargs)

    def calculate_prices(self, menus=None):
        Menu = self.menu_dinner.__class__
        if self._state.adding:
            if menus is None:
                menus = self.get_menus()
            has_zero_price = any(menu.net_price == Decimal('0') for menu in menus)
            net_price = Decimal(
                0 if has_zero_price else sum(menu.net_price for menu in menus if menu)
            )
        else:
            has_zero_price_menu = Menu.objects.filter(
                Q(pk=OuterRef("menu_breakfast_id"))
                | Q(pk=OuterRef("menu_lunch_id"))
                | Q(pk=OuterRef("menu_dinner_id")),
                net_price=0,
            )

            net_price_qs = (
                Recipe.objects.filter(pk=self.pk)
                .annotate(
                    has_zero_price=Exists(has_zero_price_menu),
                    total_price=(
                        Coalesce(
                            F("menu_breakfast__net_price"),
                            Value(0),
                            output_field=DecimalField(),
                        )
                        + Coalesce(
                            F("menu_lunch__net_price"),
                            Value(0),
                            output_field=DecimalField(),
                        )
                        + Coalesce(
                            F("menu_dinner__net_price"),
                            Value(0),
                            output_field=DecimalField(),
                        )
                    ),
                )
                .values("has_zero_price", "total_price")
                .first()
            )

            if not net_price_qs:
                net_price = Decimal(0)
            elif net_price_qs["has_zero_price"]:
                net_price = Decimal(0)
            else:
                net_price = net_price_qs["total_price"] or Decimal(0)

        # Round to 2 decimal places with ROUND_HALF_UP
        self.net_price = net_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.gross_price = (
            (self.net_price + self.profit).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            if net_price > Decimal('0')
            else Decimal(0)
        )
