from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.foods.models import RecipeFood


class RecipeFoodSerializer(CustomModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = RecipeFood
        exclude = ["created_at", "created_by", "updated_at", "updated_by"]
        read_only_fields = ["price", "status"]


class RecipeUpdateFoodSerializer(CustomModelSerializer):

    class Meta:
        model = RecipeFood
        exclude = ["created_at", "created_by", "updated_at", "updated_by", "product"]
        read_only_fields = ["price", "status"]
