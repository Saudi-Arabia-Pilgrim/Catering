from apps.base.serializers import CustomModelSerializer
from apps.menus.models import Recipe


class RecipeSerializer(CustomModelSerializer):
    class Meta:
        model = Recipe
        exclude = ["slug", "created_at", "created_by", "updated_at", "updated_by"]
        read_only_fields = ["net_price", "gross_price", "status"]