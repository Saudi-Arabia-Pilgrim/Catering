from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.rooms.models.room_type import RoomType
from apps.rooms.serializers.room_type import RoomTypeSerializer


class RoomTypeListsAPIView(CustomGenericAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=200)


class RoomTypeCreateAPIView(CustomGenericAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class RoomTypeRetrieveAPIView(CustomGenericAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)


class RoomTypeUpdateAPIView(CustomGenericAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    def get(self, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


class RoomTypeDeleteAPIView(CustomGenericAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    def get(self, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)