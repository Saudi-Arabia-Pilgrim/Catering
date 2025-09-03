from rest_framework import serializers
from apps.base.serializers import AbstractCustomSerializerMixin, CustomModelSerializer
from apps.expenses.models.hiring import HiringExpense

class HiringExpenseSerializer(CustomModelSerializer):
    """
    Serializer for the HiringExpense model.
    """
    class Meta:
        model = HiringExpense
        fields = [
            "id",
            "user",
            "title",
            "date",
            "cost",
            "status"
        ]
        read_only_fields = ("created_at", "updated_at", "created_by", "updated_by")
        extra_kwargs = {
            "user": {"required": False},
            "status": {"required": False},
        }

