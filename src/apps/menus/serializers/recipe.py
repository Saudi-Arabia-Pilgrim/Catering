from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.menus.models import Recipe
from apps.menus.utils.missing_products import calculate_missing_products_for_recipe, calculate_missing_products_batch_recipes


class RecipeSerializer(CustomModelSerializer):
    missing_products = serializers.SerializerMethodField(read_only=True)

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

    def get_missing_products(self, obj):
        """
        Return missing products when recipe status is False.
        Uses cached batch data if available, otherwise falls back to individual calculation.
        """
        if not obj.status:
            # Use cached batch data if available
            if hasattr(self, '_missing_products_cache') and self._missing_products_cache is not None:
                return self._missing_products_cache.get(obj.id, {})
            # Fallback to individual calculation
            return calculate_missing_products_for_recipe(obj)
        return {}


class OptimizedRecipeSerializer(CustomModelSerializer):
    """
    Optimized version of RecipeSerializer that uses batch processing
    to avoid N+1 queries when serializing multiple recipe objects.
    """
    missing_products = serializers.SerializerMethodField(read_only=True)

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
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store batch missing products data for efficient access
        self._missing_products_cache = None
        if hasattr(self, 'context') and 'missing_products_batch' in self.context:
            self._missing_products_cache = self.context['missing_products_batch']

    def get_missing_products(self, obj):
        """
        Return missing products when recipe status is False.
        Uses cached batch data if available, otherwise falls back to individual calculation.
        """
        if not obj.status:
            # Use cached batch data if available
            if self._missing_products_cache is not None:
                return self._missing_products_cache.get(obj.id, {})
            # Fallback to individual calculation
            return calculate_missing_products_for_recipe(obj)
        return {}

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
