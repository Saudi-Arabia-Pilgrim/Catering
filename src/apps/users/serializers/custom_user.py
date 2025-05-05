from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.expenses.models import MonthlySalary
from apps.expenses.serializers import HiringExpense


class UserSerializer(CustomModelSerializer):
    """
    Serializer for custom user model
    """
    hiring_expense = serializers.SerializerMethodField(read_only=True)
    monthly_salary = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id', 'email', 'full_name', 'phone_number', 'birthdate', 'gender',
            'role', 'is_active', 'is_staff', 'is_superuser', 'total_expenses', 'hiring_expense', 'monthly_salary'
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    async def get_hiring_expense(self, obj):
        """
        Calculates the total hiring expense for a given user object. The method fetches
        hiring expenses associated with the provided user asynchronously, processes the
        costs, and returns the total.
        """
        hiring_expenses = await sync_to_async(HiringExpense.objects.filter)(user=obj)
        hiring_expenses_total = []
        for expense in hiring_expenses:
            hiring_expenses_total.append(expense.cost)
        return sum(hiring_expenses_total) if hiring_expenses_total else 0.00

    async def get_monthly_salary(self, obj):
        """
        Add monthly salary to serializer from MonthlySalary model
        """
        monthly_salary = await sync_to_async(MonthlySalary.objects.filter)(user=obj)
        return monthly_salary.salary

    async def create(self, validated_data):
        create_user = sync_to_async(get_user_model().objects.create_user)
        return await create_user(**validated_data)

    async def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        update_user = sync_to_async(super().update)
        user = await update_user(instance, validated_data)
        if password:
            set_password = sync_to_async(user.set_password)
            await set_password(password)
            save_user = sync_to_async(user.save)
            await save_user()
        return user
