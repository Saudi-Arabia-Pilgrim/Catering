from apps.base.serializers import CustomModelSerializer
from apps.guests.models import GuestGroup


class GuestGroupListSerializer(CustomModelSerializer):
    class Meta:
        model = GuestGroup
        fields = [
            "id",
            "name",
            "count",
            'guest_group_status'
        ]
        read_only_fields = ["created_at", "updated_at", "guest_group_status"]


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
            "guest_group_status"
        ]
        read_only_fields = ["created_at", "updated_at", "guest_group_status"]


class GuestGroupDeleteSerializer(CustomModelSerializer):
    class Meta:
        model = GuestGroup
        fields = ["id"]