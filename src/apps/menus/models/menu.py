from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify

from apps.base.exceptions.exception_error import CustomExceptionError
from apps.base.models import AbstractBaseModel


class Menu(AbstractBaseModel):
    """
    A menu model representing a menu (breakfast, lunch or dinner) in a catering application.
    """

    # === The name of the menu. ===
    name = models.CharField(max_length=255)
    # === A unique slug for the menu. ===
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    # === A many-to-many relationship with the Food model. ===
    foods = models.ManyToManyField('foods.Food', related_name='menus')
    # === The count of products in the menu. ===
    count_of_products = models.PositiveSmallIntegerField()
    # === The status of the menu, default is True. ===
    status = models.BooleanField(default=True)
    # === An optional image for the menu, uploaded to 'menus/%Y/%m/%d/'. ===
    image = models.ImageField(upload_to='menus/%Y/%m/%d/', blank=True, null=True)

    # === The net price of the menu, optional. ===
    net_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, validators=[MinValueValidator(1)])
    # === The profit associated with the menu. ===
    profit = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    # === Menu price considering profit. ===
    gross_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, validators=[MinValueValidator(1)])
    
    class Meta:
        # === The database table name for the model. ===
        db_table = 'menu'
        # === The singular name for the model in the admin interface. ===
        verbose_name = 'Menu'
        # === The plural name for the model in the admin interface. ===
        verbose_name_plural = 'Menus'

    def __str__(self):
        """
        Returns a string representation of the menu, including its name, gross price, and count of products.
        """
        return f"{self.name} - {self.gross_price} - {self.count_of_products}"
    
    def clean(self):
        """
        Override the clean method to automatically generate and update the slug,
        calculate the net price, count of products, and gross price before saving
        the Menu instance. Validates the menu to ensure it contains exactly 7 foods.

        Raises:
            CustomExceptionError: If the menu does not contain exactly 7 foods.
        """
        food_queryset = self.foods.all()

        if food_queryset.count() != 7:
            raise CustomExceptionError('The menu must contain 7 foods.')

        self.slug = slugify(self.name)

        net_price_agg = food_queryset.aggregate(total_net_price=models.Sum('net_price'))
        self.net_price = net_price_agg['total_net_price'] or 0

        self.count_of_products = 7

        self.gross_price = self.net_price + self.profit

        self.status = not food_queryset.exclude(status=True).exists()