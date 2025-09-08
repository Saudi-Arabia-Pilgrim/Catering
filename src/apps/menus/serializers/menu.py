from rest_framework import serializers

from apps.base.exceptions import CustomExceptionError
from apps.base.serializers import CustomModelSerializer, CustomSerializer
from apps.foods.models import Food
from apps.menus.models import Menu


class MenuSerializer(CustomModelSerializer):

    class Meta:
        model = Menu
        exclude = ["slug", "created_at", "created_by", "updated_at", "updated_by"]
        read_only_fields = ["net_price", "gross_price", "status"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["food_count"] = instance.foods.count()
        data["foods"] = []
        request = self.context.get("request", None)
        if not request:
            raise CustomExceptionError(code=400, detail="No request found")
        for food in instance.foods.all():
            data["foods"].append(
                {
                    "id": food.id,
                    "name": food.name,
                    "price": food.gross_price,
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
        return instance

    def update(self, instance, *args, **kwargs):
        validated_data, foods = self.get_validated_data()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.foods.set(foods)
        instance.save()
        instance.change_dependent()
        return instance

    def get_foods(self, foods_id):
        foods = Food.objects.filter(id__in=foods_id)

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
