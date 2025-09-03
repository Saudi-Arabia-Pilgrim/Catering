from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.hotels.models import Hotel
from apps.rooms.serializers.rooms_of_hotel import RoomsOfHotelListSerializer
from apps.warehouses.utils import validate_uuid


class RoomsOfHotelAPIView(CustomGenericAPIView):
    serializer_class = RoomsOfHotelListSerializer

    def get(self, request, pk, *args, **kwargs):
        validate_uuid(pk)
        hotel = get_object_or_404(Hotel, pk=pk)
        rooms = hotel.rooms.all().select_related("room_type", "hotel").prefetch_related("guests")
        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data, status=200)