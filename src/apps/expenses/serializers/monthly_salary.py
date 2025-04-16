from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.expenses.models import MonthlySalary

class MonthlySalarySerializer(CustomModelSerializer):
    month_year = serializers.CharField(read_only=True)
    month = serializers.IntegerField(read_only=True)
    year = serializers.IntegerField(read_only=True)

    class Meta:
        model = MonthlySalary
        fields = ['id', 'month', 'year', 'month_year', 'salary', 'status']
