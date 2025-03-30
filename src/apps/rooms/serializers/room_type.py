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
        extra_kwargs = {
            "id": {"read_only": True}
        }

    def create(self, validated_data):
        instance = RoomType.objects.create(**validated_data)
        return instance