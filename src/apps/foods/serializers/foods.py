from django.db import connection

from rest_framework import serializers

from apps.base.exceptions import CustomExceptionError
from apps.base.serializers import CustomModelSerializer
from apps.foods.models import Food


class FoodSerializer(CustomModelSerializer):
    recipe_foods = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Food
        exclude = ["slug", "created_at", "created_by", "updated_at", "updated_by"]
        read_only_fields = ["status", "gross_price", "net_price", ]

    def validate(self, attrs):
        recipes = attrs.get("recipes", [])
        if len(recipes) == 0:
            raise CustomExceptionError(code=400, detail="At least one recipe must be provided.")
        print(len(connection.queries), "validateda")
        return attrs

    def save(self, **kwargs):
        print(len(connection.queries))
        instance = super().save(**kwargs)
        print(len(connection.queries))
        instance = Food.objects.prefetch_related("recipes", "recipes__product").get(id=instance.id)
        instance.change_dependent()
        return instance
    
    def get_recipe_foods(self, obj):
        recipes = obj.recipes.all()
        return [f"{recipe.product.name}-{recipe.count}" for recipe in recipes]