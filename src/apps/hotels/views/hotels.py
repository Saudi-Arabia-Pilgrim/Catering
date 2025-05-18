from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from apps.guests.models import Guest
from apps.hotels.models import Hotel
from apps.base.views import CustomGenericAPIView
from apps.hotels.filters import RoomWithGuestFilter
from apps.hotels.serializers import HotelSerializer, HotelListSerializer, HotelRetrieveSerializer
from apps.rooms.admin import RoomType
from apps.rooms.models import Room


class HotelListAPIView(CustomGenericAPIView):
    """
    API view to retrieve a list of hotels filtered by room type name.
    """
    queryset = Hotel.objects.prefetch_related("guests", "rooms").all()

    serializer_class = HotelListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["name__icontains"]

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

     **Endpoint**:
    `GET /api/v1/hotels/<uuid:id>/`

    **Query Parameters**:
        - `room_type` (optional, UUID): If provided, only guests staying in rooms
          of the specified room type will be included in the response.

     **Example Request**:
        GET /api/v1/hotels/14690dfa-f331-405a-aeea-61cfd429ee64/

    **Example Request with Filtering by Room Type**:
        GET /api/v1/hotels/14690dfa-f331-405a-aeea-61cfd429ee64/?room_type=134a7b13-924f-4e16-825c-86eb07a1a2ee
    """
    queryset = Hotel.objects.prefetch_related("rooms", "guests")
    serializer_class = HotelRetrieveSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={"request": request})
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
