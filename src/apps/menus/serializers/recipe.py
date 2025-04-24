from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.menus.models import Recipe


class RecipeSerializer(CustomModelSerializer):
    menu_breakfast_name = serializers.CharField(
        source="menu_breakfast.name", read_only=True
    )
    menu_lunch_name = serializers.CharField(source="menu_lunch.name", read_only=True)
    menu_dinner_name = serializers.CharField(source="menu_dinner.name", read_only=True)

    class Meta:
        model = Recipe
        exclude = ["slug", "created_at", "created_by", "updated_at", "updated_by"]
        read_only_fields = ["net_price",
                            "gross_price",
                            "status",
                            # "name"
                            ]
        # required_fields = ["name_uz", "name_ru", "name_ar", "name_en"]
