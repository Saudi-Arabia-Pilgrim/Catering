from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.rooms.models import Room
from apps.rooms.serializers import RoomSerializer


class RoomsOfHotelListAPIView(CustomGenericAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=200)


class RoomOfHotelCreateAPIView(CustomGenericAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room = serializer.save()

        response_data = {
            "id": room.id,
            "hotel": room.hotel.name,
            "counts": room.count,
            "occupied_count": room.occupied_count,
            "available_count": room.available_count,
            "price": room.price
        }

        return Response(response_data, status=201)


class RoomOfHotelRetrieveAPIView(CustomGenericAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)


class RoomOfHotelUpdateAPIView(CustomGenericAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    def patch(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


class RoomOfHotelDeleteAPIView(CustomGenericAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    def delete(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)