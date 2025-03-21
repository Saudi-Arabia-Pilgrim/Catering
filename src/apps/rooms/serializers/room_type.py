from apps.base.serializers import CustomModelSerializer
from apps.rooms.models.room_type import RoomType


class RoomTypeSerializer(CustomModelSerializer):
    class Meta:
        model = RoomType
        fields = [
            "id",
            "name",
            "status",
            "created_at"
        ]
        read_only_fields = ["created_at"]
