from apps.base.views import CustomListAPIView
from apps.rooms.models import RoomType
from apps.rooms.serializers import RoomTypeSerializer


class HotelRoomTypesAPIView(CustomListAPIView):
    serializer_class = RoomTypeSerializer

    def get_queryset(self):
        hotel_id = self.request.query_params.get("hotel")
        if not hotel_id:
            return RoomType.objects.none()

        return RoomType.objects.filter(
            rooms__hotel_id=hotel_id
        ).distinct()