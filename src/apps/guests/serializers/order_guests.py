from rest_framework import serializers

from apps.guests.models import Guest
from apps.base.exceptions import CustomExceptionError
from apps.base.serializers import CustomModelSerializer
from apps.guests.utils.calculate_price import calculate_guest_price


class GuestBaseSerializer(CustomModelSerializer):
    class Meta:
        model = Guest
        fields = "__all__"
        read_only_fields = ["order_number", "price", "created_at"]

    def validate(self, attrs):
        check_in = attrs.get("check_in")
        check_out = attrs.get("check_out")
        count = attrs.get("count", 1)
        room = attrs.get("room")

        if check_in and check_out and check_out <= check_in:
            raise CustomExceptionError(code=404, detail="Check-out check-in dan keyin bo‘lishi kerak.")

        if room and count > room.capacity:
            raise CustomExceptionError(code=404, detail="Bu xonaga bucha kishi joylasholmaydi.")

        return attrs


class GuestCreateSerializer(GuestBaseSerializer):

    def create(self, validated_data):
        guest = Guest.objects.create(**validated_data)
        calculate_guest_price(guest)
        guest.save(update_fields=["price"])
        guest.room.refresh_occupancy()
        return guest


class GuestUpdateSerializer(GuestBaseSerializer):

    def update(self, instance, validated_data):
        if instance.status == Guest.Status.COMPLETED:
            raise CustomExceptionError(code=404, detail="Tugatildigan mehmonni o‘zgartirib bo‘lmaydi.")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        calculate_guest_price(instance)
        instance.save()
        instance.room.refresh_occupancy()
        return instance


class GuestListSerializer(GuestBaseSerializer):
    class Meta:
        model = Guest
        fields = [
            "id", "order_number", "hotel", "room", "status",
            "gender", "full_name", "count", "price",
            "check_in", "check_out", "created_at"
        ]


class OrderGuestSerializer(CustomModelSerializer):
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Guest
        fields = [
            "id",
            "full_name",
            "hotel",
            "room",
            "gender",
            "price",
            "duration",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "order_number",
            "price",
            "created_at",
        ]

    def get_duration(self, obj):
        days = (obj.check_out - obj.check_in).days
        return f"{days} day"

    def get_total_price(self, obj):
        return obj.total_price

# class GuestForHotelOrderSerializer(CustomModelSerializer):
#     """
#     Serializer for the Guest model.
#
#     This serializer handles guest-related data, including retrieving guest details
#     and creating new guest entries with an associated hotel.
#     """
#     room_type = serializers.SerializerMethodField()
#     total_price = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Guest
#         fields = [
#             "id",
#             "full_name",
#             "order_number",
#             "room",
#             "room_type",
#             "gender",
#             "check_in",
#             "check_out",
#             "total_price"
#         ]
#         read_only_fields = ["order_number", "price", "room_type"]
#
#     def get_room_type(self, obj):
#         if hasattr(obj, 'room') and hasattr(obj.room, 'room_type'):
#             return obj.room.room_type.name
#         return obj.room.room_type.name if obj.room_id else None
#
#     def get_total_price(self, obj):
#         if obj.check_in and obj.check_out and obj.room:
#             days_stayed = (obj.check_out - obj.check_in).days
#             if days_stayed < 1:
#                 days_stayed = 1
#             return obj.room.gross_price * days_stayed
#         return 0
#
#
# class GuestHotelSerializer(CustomModelSerializer):
#     room_type = serializers.SerializerMethodField()
#     total_price = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Guest
#         fields = [
#             "id",
#             "full_name",
#             "order_number",
#             "room_type",
#             "gender",
#             "check_in",
#             "check_out",
#             "total_price"
#         ]
#         read_only_fields = ["order_number", "price", "room_type"]
#
#     def get_room_type(self, obj):
#         if hasattr(obj, 'room') and hasattr(obj.room, 'room_type'):
#             return obj.room.room_type.name
#         return obj.room.room_type.name if obj.room_id else None
#
#     def get_total_price(self, obj):
#         if obj.check_in and obj.check_out and obj.room:
#             days_stayed = (obj.check_out - obj.check_in).days
#             if days_stayed < 1:
#                 days_stayed = 1
#             return obj.room.gross_price * days_stayed
#         return 0
