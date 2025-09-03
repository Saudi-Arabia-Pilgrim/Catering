from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.menus.models import Recipe


class RecipeSerializer(CustomModelSerializer):

    class Meta:
        model = Recipe
        exclude = [
            "slug",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by",
        ]
        read_only_fields = [
            "net_price",
            "gross_price",
            "status",
            # "name"
        ]
        # required_fields = ["name_uz", "name_ru", "name_ar", "name_en"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        menus_fields = ["menu_breakfast", "menu_lunch", "menu_dinner"]
        data["menus"] = []
        data["menus_count"] = 3
        for menu_field in menus_fields:
            menu_id = data.pop(menu_field) 
            menu = getattr(instance, menu_field)
            data["menus"].append({menu_field: {"id": menu.id, "name": menu.name, "price": menu.gross_price}})
        return data
