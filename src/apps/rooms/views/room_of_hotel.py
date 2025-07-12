from rest_framework.response import Response

from apps.rooms.models.rooms import Room
from apps.base.views import CustomGenericAPIView
from apps.rooms.serializers import RoomUpdateSerializer
from apps.rooms.services import update_rooms_price, create_additional_rooms, delete_excess_rooms
from apps.rooms.utils.room_format import get_grouped_room_data
from apps.rooms.serializers.room import RoomSerializer, RoomCreateSerializer


class RoomListsAPIView(CustomGenericAPIView):
    serializer_class = RoomSerializer

    def get(self, *args, **kwargs):
        data = get_grouped_room_data()

        page = self.paginate_queryset(data)
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data, status=200)


class RoomCreateAPIView(CustomGenericAPIView):
    queryset = Room.objects.all().select_related("hotel", "room_type")
    serializer_class = RoomCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        rooms = serializer.save()

        response_serializer = self.get_serializer(rooms, many=True)

        return Response(response_serializer.data, status=201)


class RoomRetrieveAPIView(CustomGenericAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)


class RoomUpdateAPIView(CustomGenericAPIView):
    queryset = Room.objects.select_related("room_type", "hotel")
    serializer_class = RoomUpdateSerializer

    def get(self, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        rooms = Room.objects.filter(
            room_type=instance.room_type,
            hotel=instance.hotel
        ).order_by("created_at")

        existing_count = rooms.count()
        new_count = validated_data.get("count", existing_count)

        update_rooms_price(rooms, validated_data)

        if new_count > existing_count:
            create_additional_rooms(instance, validated_data, new_count, existing_count)
        elif new_count < existing_count:
            delete_excess_rooms(rooms, new_count, existing_count)

        return Response({
            "detail": "Rooms updated successfully",
            "room_type": instance.room_type.name,
            "hotel": instance.hotel.name,
            "new_count": new_count
        }, status=200)


class RoomDeleteAPIView(CustomGenericAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_busy:
            return Response({"detail": "This room was busy."})
        instance.delete()
        return Response(status=204)