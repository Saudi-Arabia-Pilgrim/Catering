from apps.base.serializers import CustomModelSerializer
from apps.rooms.models.rooms import Room


class RoomSerializer(CustomModelSerializer):
    class Meta:
        model = Room
        fields = [
            "id",
            "room_type",
            "created_at",
            "status"
        ]