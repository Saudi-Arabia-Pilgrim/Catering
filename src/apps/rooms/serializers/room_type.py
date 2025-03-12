from apps.base.serializers import CustomModelSerializer
from apps.rooms.models.room_type import RoomType


class RoomTypeSerializer(CustomModelSerializer):
    """
    Serializer for the RoomType model.

    This serializer handles the serialization and deserialization of room types,
    including their ID, name, creation timestamp, and status.

    Attributes:
        id (int): Unique identifier for the room type.
        name (str): The name of the room type (e.g., Single, Double, Suite).
        created_at (datetime): The timestamp when the room type was created.
        status (bool): Indicates whether the room type is active or not.
    """

    class Meta:
        model = RoomType
        fields = [
            "id",
            "name",
            "created_at",
            "status"
        ]
