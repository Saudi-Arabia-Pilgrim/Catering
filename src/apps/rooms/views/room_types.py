from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from apps.base.views import CustomGenericAPIView
from apps.rooms.filters import RoomTypeFilter
from apps.rooms.models.room_type import RoomType
from apps.rooms.serializers.room_type import RoomTypeSerializer


class RoomTypeListsAPIView(CustomGenericAPIView):
    """
      API View to list all room types with optional search by name.

      This endpoint provides a list of all available room types.
      You can search by room type name using the `search` query parameter.

      🔍 Search:
      - Search by room type name (case-insensitive):
          • Example: `?search=deluxe`

      ⚠️ Dear Frontend Developers:
      These docstrings are written with love 💙
      Please read them carefully so we don't have to repeat ourselves in meetings 😄
    """
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = RoomTypeFilter
    search_fields = ["name__icontains"]

    def get(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
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