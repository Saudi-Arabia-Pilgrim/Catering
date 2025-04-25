from apps.base.serializers import CustomModelSerializer
from apps.transports.models import Transport

class TransportSerializer(CustomModelSerializer):
    """
    Serializer for the Transport model.
    """
    class Meta:
        model = Transport
        fields = [
            'id', 'name', 'name_of_driver', 'address',
            'phone_number', 'amount_of_people', 'status',
            'created_at', 'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by')
