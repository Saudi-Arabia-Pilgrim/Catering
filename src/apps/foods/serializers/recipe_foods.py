from apps.base.serializers import CustomModelSerializer
from apps.foods.models import RecipeFood


class RecipeFoodSerializer(CustomModelSerializer):
    class Meta:
        model = RecipeFood
        exclude = ["created_at", "created_by", "updated_at", "updated_by"]
        read_only_fields = ["price", "status"]