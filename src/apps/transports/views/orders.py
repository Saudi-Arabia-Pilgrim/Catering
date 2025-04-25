from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from apps.base.views.generics import (CustomCreateAPIView, CustomListAPIView, CustomRetrieveUpdateDestroyAPIView)
from apps.transports.filters import OrderFilter
from apps.transports.models import Order
from apps.transports.serializers import OrderSerializer


class OrderListAPIView(CustomListAPIView):
    """
    API view for listing and filtering orders.
    """
    is_authenticated = True
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = OrderFilter
    search_fields = ['from_location', 'to_location', 'order_number', 'status', 'passenger_count']



class OrderCreateAPIView(CustomCreateAPIView):
    """
    API view for creating a new taxi order.
    """
    is_authenticated = True
    serializer_class = OrderSerializer
    queryset = Order.objects.all()



class OrderRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
