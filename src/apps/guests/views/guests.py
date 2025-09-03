from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.base.views import CustomListAPIView, CustomRetrieveAPIView, CustomGenericAPIView
from apps.guests.models import Guest
from apps.guests.serializers import GuestListSerializer
from apps.hotels.models import Hotel
from apps.warehouses.utils import validate_uuid


class GuestListAPIView(CustomListAPIView):
    serializer_class = GuestListSerializer
    queryset = Guest.objects.all()


class GuestOfHotelListAPIView(CustomRetrieveAPIView):
    serializer_class = GuestListSerializer
    queryset = Guest.objects.all()

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        validate_uuid(pk)
        hotel = get_object_or_404(Hotel, pk=pk)
        guests = self.get_queryset().filter(hotel=hotel)
        serializer = self.get_serializer(guests, many=True)
        return Response(serializer.data)
