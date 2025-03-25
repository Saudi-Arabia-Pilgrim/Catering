from apps.base.exceptions import CustomExceptionError
from apps.base.serializers import CustomModelSerializer
from apps.menus.models import Menu


class MenuSerializer(CustomModelSerializer):
    class Meta:
        model = Menu
        exclude = ["slug", "created_at", "created_by", "updated_at", "updated_by"]
        read_only_fields = ["net_price", "gross_price", "status"]

    def validate(self, attrs):
        foods = attrs.get('foods', [])
        if len(foods) != 7:
            raise CustomExceptionError(code=400, detail="One menu can only have 7 dishes")
        return attrs
    
    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.change_dependent()
        return instance