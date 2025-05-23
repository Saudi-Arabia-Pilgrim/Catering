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

    def get_hiring_expense(self, obj):
        """
        Calculates the total hiring expense for a given user object. The method fetches
        hiring expenses associated with the provided user asynchronously, processes the
        costs, and returns the total.
        """
        hiring_expenses = HiringExpense.objects.filter(user=obj)
        hiring_expenses_total = []
        for expense in hiring_expenses:
            hiring_expenses_total.append(expense.cost)
        return sum(hiring_expenses_total) if hiring_expenses_total else 0.00

    def get_monthly_salary(self, obj):
        """
        Add monthly salary to serializer from MonthlySalary model
        """
        monthly_salary = MonthlySalary.objects.filter(user=obj).first()
        return monthly_salary.salary if monthly_salary else None

    def create(self, validated_data):
        create_user = get_user_model().objects.create_user
        return create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        update_user = super().update
        user = update_user(instance, validated_data)
        if password:
            set_password = user.set_password
            set_password(password)
            save_user = user.save
            save_user()
        return user
