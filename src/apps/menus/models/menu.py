from django.db import models

from apps.base.models import AbstractBaseModel


class Menu(AbstractBaseModel):
    """
    A menu model representing a menu (breakfast, lunch or dinner) in a catering application.
    """

    # === The name of the menu. ===
    name = models.CharField(max_length=255)
    # === A many-to-many relationship with the Food model. ===
    food = models.ManyToManyField('foods.Food', related_name='menus')
    # === The count of products in the menu. ===
    count_of_products = models.FloatField()
    # === The status of the menu, default is True. ===
    status = models.BooleanField(default=True)
    # === An optional image for the menu, uploaded to 'menus/%Y/%m/%d/'. ===
    image = models.ImageField(upload_to='menus/%Y/%m/%d/', blank=True, null=True)

    # === The net price of the menu, optional. ===
    net_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    # === The profit associated with the menu. ===
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    # === Menu price considering profit. ===
    gross_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    
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