from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.rooms.models.rooms import Room
from apps.rooms.serializers.room import RoomSerializer, RoomCreateSerializer


class RoomListsAPIView(CustomGenericAPIView):
    queryset = Room.objects.all().select_related("room_type")
    serializer_class = RoomSerializer

    def get(self, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=200)


class RoomCreateAPIView(CustomGenericAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class RoomRetrieveAPIView(CustomGenericAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)


class RoomUpdateAPIView(CustomGenericAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

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


class RoomDeleteAPIView(CustomGenericAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)