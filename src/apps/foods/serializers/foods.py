from rest_framework import serializers

from apps.base.exceptions import CustomExceptionError
from apps.base.serializers import CustomModelSerializer, CustomSerializer
from apps.foods.models import Food, RecipeFood, FoodSection
from apps.foods.serializers.recipe_foods import RecipeFoodSerializer
from apps.foods.utils.missing_products import calculate_missing_products_for_food, calculate_missing_products_batch


class FoodSectionSerializer(CustomModelSerializer):
    class Meta:
        model = FoodSection
        fields = [
            "id",
            "name",
            "status",
            "created_at"
        ]


class FoodSerializer(CustomModelSerializer):
    recipe_foods = serializers.SerializerMethodField(read_only=True)
    section_name = serializers.SerializerMethodField(read_only=True)
    missing_products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Food
        exclude = ["slug", "created_at", "created_by", "updated_at", "updated_by"]
        read_only_fields = [
            "status",
            "gross_price",
            "net_price",
            # "name"
        ]
        # required_fields = ["name_uz", "name_ru", "name_ar", "name_en"]

    def get_recipe_foods(self, obj):
        # Use prefetched recipes to avoid N+1 queries
        recipes = obj.recipes.all()
        return RecipeFoodSerializer(recipes, many=True).data

    def get_section_name(self, obj):
        # Use prefetched section to avoid N+1 queries
        return obj.section.name

    def get_missing_products(self, obj):
        """
        Return missing products when food status is False.

        Returns:
            dict: Dictionary with product names as keys and missing quantities as values
                  Example: {"Product Name": 5.25, "Another Product": 2.00}
        """
        if not obj.status:
            return calculate_missing_products_for_food(obj)
        return {}


class OptimizedFoodSerializer(CustomModelSerializer):
    """
    Optimized version of FoodSerializer that uses batch processing
    to avoid N+1 queries when serializing multiple food objects.
    """
    recipe_foods = serializers.SerializerMethodField(read_only=True)
    section_name = serializers.SerializerMethodField(read_only=True)
    missing_products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Food
        exclude = ["slug", "created_at", "created_by", "updated_at", "updated_by"]
        read_only_fields = [
            "status",
            "gross_price",
            "net_price",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store batch missing products data for efficient access
        self._missing_products_cache = None
        if hasattr(self, 'context') and 'missing_products_batch' in self.context:
            self._missing_products_cache = self.context['missing_products_batch']

    def get_recipe_foods(self, obj):
        # Use prefetched recipes to avoid N+1 queries
        recipes = obj.recipes.all()
        return RecipeFoodSerializer(recipes, many=True).data

    def get_section_name(self, obj):
        # Use prefetched section to avoid N+1 queries
        return obj.section.name

    def get_missing_products(self, obj):
        """
        Return missing products when food status is False.
        Uses cached batch data if available, otherwise falls back to individual calculation.
        """
        if not obj.status:
            # Use cached batch data if available
            if self._missing_products_cache is not None:
                return self._missing_products_cache.get(obj.id, {})
            # Fallback to individual calculation
            return calculate_missing_products_for_food(obj)
        return {}


class FoodSerializerForFoodOrder(CustomModelSerializer):
    class Meta:
        model = Food
        exclude = ["slug", "created_at", "created_by", "updated_at", "updated_by", "recipes"]
        read_only_fields = [
            "status",
            "gross_price",
            "net_price",
            # "name",
        ]
        # required_fields = ["name_uz", "name_ru", "name_ar", "name_en"]


class FoodCreateUpdateSerializer(CustomSerializer):

    name = serializers.CharField()
    recipes_id = serializers.ListField(write_only=True)
    section = serializers.PrimaryKeyRelatedField(queryset=FoodSection.objects.filter(status=True))
    profit = serializers.DecimalField(max_digits=10, decimal_places=2)
    image = serializers.ImageField(required=False, allow_null=True)

    def validate(self, attrs):
        recipes = attrs.get("recipes_id", [])
        if len(recipes) == 0:
            raise CustomExceptionError(
                code=400, detail="At least one recipe must be provided."
            )
        return attrs

    def create(self, *args, **kwargs):
        validated_data, recipe_foods = self.get_validated_data()
        instance = Food.objects.create(**validated_data)
        instance.recipes.set(recipe_foods)
        instance.change_dependent()
        return instance

    def update(self, instance, *args, **kwargs):
        validated_data, recipe_foods = self.get_validated_data()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.recipes.set(recipe_foods)
        instance.save()
        instance.change_dependent()
        return instance

    def get_recipes(self, recipe_foods_id):
        recipe_foods = RecipeFood.objects.filter(id__in=recipe_foods_id)

        if len(recipe_foods) != len(recipe_foods_id):
            raise CustomExceptionError(
                code=400, detail="Some recipe IDs are invalid or do not exist."
            )

        return recipe_foods

    def get_validated_data(self):
        validated_data = self.validated_data.copy()
        recipe_foods_id = validated_data.pop("recipes_id", None)

        if recipe_foods_id is None:
            raise CustomExceptionError(code=400, detail="No recipe IDs were provided.")

        recipe_foods = self.get_recipes(recipe_foods_id)
        return validated_data, recipe_foods
