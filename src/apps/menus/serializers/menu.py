from rest_framework import serializers

from apps.base.exceptions import CustomExceptionError
from apps.base.serializers import CustomModelSerializer, CustomSerializer
from apps.foods.models import Food
from apps.menus.models import Menu
from apps.menus.utils.missing_products import calculate_missing_products_for_menu, calculate_missing_products_batch_menus


class MenuSerializer(CustomModelSerializer):
    missing_products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Menu
        exclude = ["slug", "created_at", "created_by", "updated_at", "updated_by"]
        read_only_fields = ["net_price", "gross_price", "status"]

    def get_missing_products(self, obj):
        """
        Return missing products when menu status is False.
        Uses cached batch data if available, otherwise falls back to individual calculation.
        """
        if not obj.status:
            # Use cached batch data if available
            if hasattr(self, '_missing_products_cache') and self._missing_products_cache is not None:
                return self._missing_products_cache.get(obj.id, {})
            # Fallback to individual calculation
            return calculate_missing_products_for_menu(obj)
        return {}

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Use prefetched foods to avoid N+1 queries
        foods = instance.foods.all()
        data["food_count"] = len(foods)
        data["foods"] = []

        request = self.context.get("request", None)
        if not request:
            raise CustomExceptionError(code=400, detail="No request found")

        for food in foods:
            data["foods"].append(
                {
                    "id": food.id,
                    "name": food.name,
                    "price": str(food.gross_price),
                    "image": (
                        request.build_absolute_uri(food.image.url)
                        if food.image
                        else None
                    ),
                }
            )
        return data


class OptimizedMenuSerializer(CustomModelSerializer):
    """
    Optimized version of MenuSerializer that uses batch processing
    to avoid N+1 queries when serializing multiple menu objects.
    """
    missing_products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Menu
        exclude = ["slug", "created_at", "created_by", "updated_at", "updated_by"]
        read_only_fields = ["net_price", "gross_price", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store batch missing products data for efficient access
        self._missing_products_cache = None
        if hasattr(self, 'context') and 'missing_products_batch' in self.context:
            self._missing_products_cache = self.context['missing_products_batch']

    def get_missing_products(self, obj):
        """
        Return missing products when menu status is False.
        Uses cached batch data if available, otherwise falls back to individual calculation.
        """
        if not obj.status:
            # Use cached batch data if available
            if self._missing_products_cache is not None:
                return self._missing_products_cache.get(obj.id, {})
            # Fallback to individual calculation
            return calculate_missing_products_for_menu(obj)
        return {}

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Use prefetched foods to avoid N+1 queries
        foods = instance.foods.all()
        data["food_count"] = len(foods)
        data["foods"] = []

        request = self.context.get("request", None)
        if not request:
            raise CustomExceptionError(code=400, detail="No request found")

        for food in foods:
            data["foods"].append(
                {
                    "id": food.id,
                    "name": food.name,
                    "price": str(food.gross_price),
                    "image": (
                        request.build_absolute_uri(food.image.url)
                        if food.image
                        else None
                    ),
                }
            )
        return data


class MenuCreateUpdateSerializer(CustomSerializer):

    name = serializers.CharField()
    foods_id = serializers.ListField(write_only=True)
    profit = serializers.DecimalField(max_digits=10, decimal_places=2)
    image = serializers.ImageField(required=False, allow_null=True)
    menu_type = serializers.ChoiceField(choices=Menu.MenuType.choices)

    def validate(self, attrs):
        foods = attrs.get("foods_id", [])
        if len(foods) != 7:
            raise CustomExceptionError(
                code=400, detail="One menu can only have 7 dishes"
            )
        return attrs

    def create(self, *args, **kwargs):
        validated_data, foods = self.get_validated_data()
        instance = Menu.objects.create(**validated_data)
        instance.foods.set(foods)
        instance.change_dependent()

        # Refresh instance with prefetched data to avoid N+1 queries
        instance = Menu.objects.prefetch_related(
            'foods__recipes__product'
        ).get(pk=instance.pk)

        return instance

    def update(self, instance, *args, **kwargs):
        validated_data, foods = self.get_validated_data()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.foods.set(foods)
        instance.save()
        instance.change_dependent()

        # Refresh instance with prefetched data to avoid N+1 queries
        instance = Menu.objects.prefetch_related(
            'foods__recipes__product'
        ).get(pk=instance.pk)

        return instance

    def get_foods(self, foods_id):
        # Prefetch related data to avoid N+1 queries when serializing
        foods = Food.objects.filter(id__in=foods_id).prefetch_related(
            'recipes__product'
        )

        if len(foods) != len(foods_id):
            raise CustomExceptionError(
                code=400, detail="Some recipe IDs are invalid or do not exist."
            )

        return foods

    def get_validated_data(self):
        validated_data = self.validated_data.copy()
        foods_id = validated_data.pop("foods_id", None)

        if foods_id is None:
            raise CustomExceptionError(code=400, detail="No recipe IDs were provided.")

        foods = self.get_foods(foods_id)
        return validated_data, foods
