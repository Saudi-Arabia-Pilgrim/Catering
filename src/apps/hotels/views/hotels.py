from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter


from apps.rooms.models import Room
from apps.hotels.models import Hotel
from apps.guests.models import Guest
from apps.base.views import CustomGenericAPIView
from apps.hotels.filters import RoomWithGuestFilter
from apps.hotels.serializers import HotelSerializer


class HotelListAPIView(CustomGenericAPIView):
    """
    API view to retrieve a list of hotels filtered by room type name.
    """

    serializer_class = HotelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = RoomWithGuestFilter
    search_fields = ["name__icontains"]

    def get_queryset(self):
        room_type_name = self.request.query_params.get("room_type_name")

        # Filter Guests
        guest_qs = Guest.objects.select_related('room', 'room__room_type').only(
            'id', 'full_name', 'order_number', 'room_id',
            'gender', 'check_in', 'check_out', 'hotel_id'
        )
        if room_type_name:
            guest_qs = guest_qs.filter(room__room_type__name__icontains=room_type_name)

        # Filter Rooms
        room_qs = Room.objects.select_related("room_type").only(
            'id', 'room_type__name', 'gross_price', 'occupied_count',
            'count', 'hotel_id', 'room_type_id', 'capacity', 'net_price'
        )
        if room_type_name:
            room_qs = room_qs.filter(room_type__name__icontains=room_type_name)

        # Filter Hotels with only matching rooms
        hotels_qs = Hotel.objects.prefetch_related(
            Prefetch("rooms", queryset=room_qs),
            Prefetch("guests", queryset=guest_qs)
        )
        if room_type_name:
            hotels_qs = hotels_qs.filter(rooms__room_type__name__icontains=room_type_name).distinct()

        return hotels_qs

    def get(self, *args, **kwargs):
        """
        Handle GET requests to return the list of hotels.
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

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
