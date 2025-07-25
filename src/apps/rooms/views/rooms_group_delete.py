from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework.response import Response

from apps.hotels.models import Hotel
from apps.rooms.services import RoomService
from apps.rooms.models import RoomType, Room
from apps.base.views import CustomGenericAPIView


class RoomGroupDeleteAPIView(CustomGenericAPIView):
    queryset = Room.objects.all()
    serializer_class = None

    @extend_schema(
        summary="Xonalarni guruh bo‘yicha o‘chirish",
        description="`hotel` va `room_type` query params asosida bo‘sh (band bo‘lmagan) xonalarni o‘chiradi.",
        parameters=[
            OpenApiParameter(
                name="hotel",
                description="Hotel ID (UUID formatda)",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                name="room_type",
                description="RoomType ID (UUID formatda)",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.QUERY
            ),
        ],
        responses={
            200: OpenApiResponse(description="O‘chirilgan xonalar soni"),
            400: OpenApiResponse(description="Notog‘ri yoki yetishmayotgan query param"),
            404: OpenApiResponse(description="Hotel yoki RoomType topilmadi"),
        }
    )
    def delete(self, request, *args, **kwargs):
        hotel_id = request.query_params.get("hotel")
        room_type_id = request.query_params.get("room_type")

        if not hotel_id or not room_type_id:
            return Response(
                {"detail": "room_type and hotel query params was not found."},
                status=400
            )

        try:
            hotel = Hotel.objects.get(id=hotel_id)
            room_type = RoomType.objects.get(id=room_type_id)
        except (RoomType.DoesNotExist, Hotel.DoesNotExist):
            return Response(
                {"detail": "RoomType or Hotel was not found."},
                status=404
            )

        deleted_count = RoomService.delete_unoccupied_rooms(hotel, room_type)

        return Response(
            {"deleted_count": deleted_count},
            status=200
        )