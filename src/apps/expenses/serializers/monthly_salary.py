from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.base.serializers import CustomModelSerializer
from apps.expenses.models import MonthlySalary

User = get_user_model()

class MonthlySalarySerializer(CustomModelSerializer):
    month_year = serializers.CharField(read_only=True)
    month = serializers.IntegerField(read_only=True)
    year = serializers.IntegerField(read_only=True)

    class Meta:
        model = MonthlySalary
        fields = ['id', 'month', 'year', 'month_year', 'salary', 'status']

class MonthlySalaryCreateSerializer(CustomModelSerializer):
    employee_id = serializers.UUIDField(write_only=True)
    month = serializers.IntegerField(write_only=True, min_value=1, max_value=12)
    year = serializers.IntegerField(write_only=True, min_value=2020)

    class Meta:
        model = MonthlySalary
        fields = ['employee_id', 'month', 'year', 'salary']

    def validate_employee_id(self, value):
        try:
            user = User.objects.get(id=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Employee with this ID does not exist.")

    def create(self, validated_data):
        from datetime import date
        
        employee_id = validated_data.pop('employee_id')
        month = validated_data.pop('month')
        year = validated_data.pop('year')
        
        # Create date for the first day of the month
        date_obj = date(year, month, 1)
        
        # Check if salary already exists for this user and month/year
        existing_salary = MonthlySalary.objects.filter(
            user_id=employee_id,
            date__year=year,
            date__month=month
        ).first()
        
        if existing_salary:
            raise serializers.ValidationError(
                f"Salary for this employee already exists for {date_obj.strftime('%B %Y')}"
            )
        
        return MonthlySalary.objects.create(
            user_id=employee_id,
            date=date_obj,
            **validated_data
        )

class MonthlySalaryUpdateSerializer(CustomModelSerializer):
    class Meta:
        model = MonthlySalary
        fields = ['salary', 'status']
        
    def validate_salary(self, value):
        if value < 0:
            raise serializers.ValidationError("Salary cannot be negative.")
        return value
