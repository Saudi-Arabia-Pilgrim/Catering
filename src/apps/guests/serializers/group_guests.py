from apps.base.serializers import CustomModelSerializer
from apps.guests.models import GuestGroup


class GuestGroupListSerializer(CustomModelSerializer):
    class Meta:
        model = GuestGroup
        fields = [
            "id",
            "name",
            "count",
        ]
        read_only_fields = ["created_at", "updated_at"]


class GuestGroupCreateSerializer(CustomModelSerializer):
    class Meta:
        model = GuestGroup
        fields = [
            "id",
            "name",
            "count",
        ]
        read_only_fields = ["created_at", "updated_at"]


class GuestGroupRetrieveUpdateSerializer(CustomModelSerializer):
    class Meta:
        model = GuestGroup
        fields = [
            "id",
            "name",
            "count",
        ]
        read_only_fields = ["created_at", "updated_at"]


class GuestGroupDeleteSerializer(CustomModelSerializer):
    class Meta:
        model = GuestGroup
        fields = ["id"]