from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.hotels.models import Hotel
from apps.hotels.serializers.hotel_booked import HotelBookedSerializer


class HotelBookedListAPIView(CustomGenericAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelBookedSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)