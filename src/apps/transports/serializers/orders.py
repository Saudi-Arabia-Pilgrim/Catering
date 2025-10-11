from rest_framework import serializers

from apps.base.serializers import CustomModelSerializer
from apps.transports.models import Order


class OrderSerializer(CustomModelSerializer):
    transport_model_name = serializers.CharField(source="transport.name", read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "transport",
            "order_number",
            "perform_date",
            "from_location",
            "to_location",
            "status",
            "passenger_count",
            "service_fee",
            "gross_fee",
            "transport_model_name",
        )
        read_only_fields = (
            "id",
            "order_number",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        )

    def validate(self, attrs):
        """
        Validate that passenger_count doesn't exceed transport's amount_of_people
        """
        transport = attrs.get('transport')
        passenger_count = attrs.get('passenger_count')

        if transport and passenger_count:
            try:
                passenger_count_int = int(passenger_count)
                amount_of_people_int = int(transport.amount_of_people)

                if passenger_count_int > amount_of_people_int:
                    raise serializers.ValidationError({
                        'passenger_count': f"Passenger count ({passenger_count_int}) exceeds the transport's capacity ({amount_of_people_int} people)."
                    })
            except ValueError:
                raise serializers.ValidationError({
                    'passenger_count': "Passenger count must be a valid number."
                })

        return attrs
