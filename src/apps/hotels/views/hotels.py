from django.db.models import Prefetch
from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from apps.base.views import CustomGenericAPIView
from apps.guests.models import Guest
from apps.hotels.models import Hotel
from apps.hotels.serializers import HotelSerializer
from apps.rooms.models import Room


class HotelListAPIView(CustomGenericAPIView):
    """
    API view to retrieve a list of hotels.

    This view fetches all hotels from the database and returns their serialized data.
    """
    queryset = Hotel.objects.prefetch_related(
        Prefetch(
            "rooms",
            queryset=Room.objects.select_related("room_type")
            .only('id', 'room_type__name', 'gross_price', 'occupied_count', 'count', 'hotel_id', 'room_type_id')
        ),
        Prefetch(
            "guests",
            queryset=Guest.objects.select_related('room', 'room__room_type')
            .only('id', 'full_name', 'order_number', 'room_id', 'gender', 'check_in', 'check_out', 'hotel_id')
        )
    ).all()
    serializer_class = HotelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["name__icontains"]

    def get(self, *args, **kwargs):
        """
        Handle GET requests to return the list of hotels.

        Returns:
            Response: A response containing the serialized list of hotels.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HotelCreateAPIView(CustomGenericAPIView):
    """
    API view to create a new hotel.
    """
    queryset = Hotel.objects.all().prefetch_related("guests", "room")
    serializer_class = HotelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        hotel = serializer.save()

        response_data = {
            "id": hotel.id,
            "name": hotel.name,
            "address": hotel.address,
            "email": hotel.email,
            "phone_number": hotel.phone_number,
            "rating": hotel.rating
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class HotelRetrieveAPIView(CustomGenericAPIView):
    """
    API view to retrieve a specific hotel.
    """
    queryset = Hotel.objects.prefetch_related(
        Prefetch(
            'rooms',
            queryset=Room.objects.select_related('room_type').only(
                'id', 'room_type_id', 'hotel_id', 'gross_price', 'occupied_count', 'count'
            )
        ),
        Prefetch(
            'guests',
            queryset=Guest.objects.select_related('room', 'room__room_type').only(
                'id', 'full_name', 'order_number', 'room_id', 'gender',
                'check_in', 'check_out', 'hotel_id'
            )
        )
    ).only("id", "name", "email", "address", "phone_number", "rating")
    serializer_class = HotelSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HotelUpdateAPIView(CustomGenericAPIView):
    """
    API view to update a specific hotel.
    """
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class HotelDeleteAPIView(CustomGenericAPIView):
    """
    API view to delete a specific hotel.
    """
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
