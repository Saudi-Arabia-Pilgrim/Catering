from decimal import ROUND_DOWN, Decimal

from django.db import models
from django.db.models import (Sum, DecimalField,Q,
                              OuterRef, Exists)
from django.core.validators import MinValueValidator
from django.utils.text import slugify

from apps.base.exceptions import CustomExceptionError
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
    # === Status of the recipe, default is True (active). ===
    status = models.BooleanField(default=True)
    # === Net price of the recipe. ===
    net_price = models.FloatField(blank=True)
    # === Profit associated with the recipe. ===
    profit = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    # === Gross price of the recipe. ===
    gross_price = models.FloatField(blank=True)

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
        return f"{self.name} - {self.gross_price}"
    
    def get_menus(self):
        menus_id = [self.menu_breakfast_id, self.menu_lunch_id, self.menu_dinner_id]
        return list(self.menu_breakfast.__class__.objects.filter(id__in=menus_id))

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        obj = self.__class__.objects.filter(slug=slug).exclude(pk=self.pk).first()
        if obj:
            raise CustomExceptionError(code=400, detail="A recipe with this name already exists")
        self.slug = slug

        menus = self.get_menus()

        self.calculate_prices(menus=menus)
        self.status = all(menu.status for menu in menus)

        super().save(*args, **kwargs)
        del menus
    
    def calculate_prices(self, menus=None):
        Menu = self.menu_dinner.__class__

        if self.pk is None:
            if menus is None:
                menus = self.get_menus()
            has_zero_price = any(menu.net_price == 0 for menu in menus)
            net_price = Decimal(0) if has_zero_price else sum(
                menu.net_price for menu in menus if menu
            )
        else:
            has_zero_price_menu = Menu.objects.filter(
                Q(pk=OuterRef("menu_breakfast_id")) |
                Q(pk=OuterRef("menu_lunch_id")) |
                Q(pk=OuterRef("menu_dinner_id")),
                net_price=0
            )

            net_price_qs = Recipe.objects.filter(pk=self.pk).annotate(
                has_zero_price=Exists(has_zero_price_menu),
                total_price=(
                    Sum("menu_breakfast__net_price", output_field=DecimalField()) +
                    Sum("menu_lunch__net_price", output_field=DecimalField()) +
                    Sum("menu_dinner__net_price", output_field=DecimalField())
                )
            ).values("has_zero_price", "total_price").first()

            if not net_price_qs:
                net_price = Decimal(0)
            elif net_price_qs["has_zero_price"]:
                net_price = Decimal(0)
            else:
                net_price = net_price_qs["total_price"] or Decimal(0)

        self.net_price = net_price.quantize(Decimal("0.0001"), rounding=ROUND_DOWN)
        self.gross_price = (
            (self.net_price + self.profit).quantize(Decimal("0.0001"), rounding=ROUND_DOWN)
            if net_price > 0 else Decimal(0)
        )