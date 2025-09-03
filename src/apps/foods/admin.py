from django.contrib import admin

from apps.foods.models import Food, RecipeFood, FoodSection

admin.site.register(Food)
admin.site.register(RecipeFood)
admin.site.register(FoodSection)
