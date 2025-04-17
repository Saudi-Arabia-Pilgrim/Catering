from rest_framework import status

from apps.base.response.responses import CustomSuccessResponse
from apps.base.views.generics import (CustomCreateAPIView, CustomRetrieveUpdateDestroyAPIView)
from apps.transports.models import Transport
from apps.transports.serializers import TransportSerializer
from apps.transports.tasks.create_new_transport import create_new_transport


class TransportCreateAPIView(CustomCreateAPIView):
    """
    API view for creating a new transport.
    """
    serializer_class = TransportSerializer
    queryset = Transport.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Override the create method to handle custom logic.
        """
        create_new_transport.delay(data=request.data, user_id=request.user.id)
        return CustomSuccessResponse(message="Transport created successfully.", status_code=status.HTTP_201_CREATED)


class TransportRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting transport.
    """
    serializer_class = TransportSerializer
    queryset = Transport.objects.all()

