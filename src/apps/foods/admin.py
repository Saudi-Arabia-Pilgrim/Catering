from django.contrib import admin

from apps.foods.models import Food, RecipeFood

admin.site.register(Food)
admin.site.register(RecipeFood)