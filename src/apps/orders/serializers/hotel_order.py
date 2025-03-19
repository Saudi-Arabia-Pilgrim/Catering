from apps.base.serializers import CustomModelSerializer
from apps.guests.serializers import GuestSerializer
from apps.orders.models.hotel_order import HotelOrder


class HotelOrderSerializer(CustomModelSerializer):
    guests = GuestSerializer(many=True, read_only=True)

    class Meta:
        model = HotelOrder
        fields = [
            "id",
            "order_id",
            "hotel",
            "room",
            "guests",
            "order_status",
            "food_service",
            "check_in",
            "check_out",
            "count_of_people",
            "general_cost",
            "created_at"
        ]
        read_only_fields = ["order_id", "general_cost"]

