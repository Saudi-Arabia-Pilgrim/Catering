from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from apps.base.views.generics import (CustomCreateAPIView, CustomRetrieveUpdateDestroyAPIView, CustomListAPIView)
from apps.transports.filters import TransportFilter
from apps.transports.models import Transport
from apps.transports.serializers import TransportSerializer


class TransportListAPIView(CustomListAPIView):
    """
    API view for listing and filtering transports.
    """
    is_authenticated = True
    serializer_class = TransportSerializer
    queryset = Transport.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = TransportFilter
    search_fields = ['name', 'name_of_driver', 'address', 'phone_number']



class TransportCreateAPIView(CustomCreateAPIView):
    """
    API view for creating a new transport.
    """
    is_authenticated = True
    serializer_class = TransportSerializer
    queryset = Transport.objects.all()



class TransportRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting transport.
    """
    serializer_class = TransportSerializer
    queryset = Transport.objects.all()
