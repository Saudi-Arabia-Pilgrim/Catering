from apps.transports.models import Transport
from apps.transports.serializers import TransportSerializer
from apps.base.views.generics import (
    CustomCreateAPIView,
    CustomRetrieveUpdateDestroyAPIView
)


class TransportCreateAPIView(CustomCreateAPIView):
    """
    API view for creating a new transport.
    """
    serializer_class = TransportSerializer
    queryset = Transport.objects.all()

class TransportRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting transport.
    """
    serializer_class = TransportSerializer
    queryset = Transport.objects.all()