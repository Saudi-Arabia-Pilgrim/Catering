from apps.base.exceptions import CustomExceptionError
from apps.base.serializers import CustomModelSerializer
from apps.foods.models import Food


class FoodSerializer(CustomModelSerializer):
    class Meta:
        model = Food
        exclude = ["slug", "created_at", "created_by", "updated_at", "updated_by"]
        read_only_fields = ["status", "gross_price", "net_price", ]

    def validate(self, attrs):
        recipes = attrs.get("recipes", [])
        if len(recipes) == 0:
            raise CustomExceptionError(code=400, detail="At least one recipe must be provided.")
        return attrs

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.change_dependent()
        return instance