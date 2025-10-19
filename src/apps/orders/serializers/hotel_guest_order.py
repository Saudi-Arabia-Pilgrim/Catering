from django.db import transaction

from rest_framework import serializers

from apps.orders.utils.calculate_price import calculate_prices_for_order
from apps.orders.utils.refresh_rooms import update_room_occupancy
from apps.rooms.models import Room
from apps.guests.models import Guest, GuestGroup
from apps.base.exceptions import CustomExceptionError
from apps.orders.models.hotel_order import HotelOrder
from apps.base.serializers import CustomModelSerializer
from apps.orders.serializers import OnlyFoodOrderSerializer
from apps.guests.utils.prepare_guests import prepare_bulk_guests
from apps.guests.serializers.order_guests import GuestListSerializer


class HotelOrderGuestSerializer(CustomModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all().select_related("hotel"), required=False)
    guests = GuestListSerializer(many=True, read_only=True)
    guest_details = serializers.ListField(write_only=True, child=serializers.DictField(), required=False)
    guest_group = serializers.UUIDField(write_only=True, required=False)
    order_status = serializers.CharField(read_only=True)
    hotel_name = serializers.CharField(source="hotel.name", read_only=True)
    guest_type = serializers.CharField(read_only=True)
    order_food = OnlyFoodOrderSerializer(source="food_order", read_only=True, many=True)

    class Meta:
        model = HotelOrder
        fields = [
            "id",
            "hotel",
            "hotel_name",
            "order_status",
            "room",
            "guest_type",
            "guests",
            "guest_details",
            "guest_group",
            "order_food",
            "food_order",
            "rooms",
            "check_in",
            "check_out",
            "count_of_people",
            "created_at",
            "order_id",
            "general_cost"
        ]
        read_only_fields = ["order_id", "general_cost"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop("food_order")
        data["total_food_price"] = 0
        data["hotel_total_price"] = data.pop("general_cost")
        data["general_cost"] = 0

        for order in data["order_food"]:
            data["total_food_price"] += order["total_price"]
            data["general_cost"] += order["total_price"]

        data["general_cost"] += data["hotel_total_price"]

        if instance.guest_group:
            data["guest_group"] = {
                "id": str(instance.guest_group.id),
                "name": instance.guest_group.name,
                "count": instance.guest_group.count,
                "guest_group_status": instance.guest_group.guest_group_status,
            }
        else:
            data["guest_group"] = None

        return data

    def validate(self, data):
        guests_data = data.get("guest_details")
        guest_group = data.get("guest_group")
        rooms = data.get("rooms")
        room = data.get("room")
        count_of_people = data.get("count_of_people") or 0



        data["guest_type"] = (
            HotelOrder.GuestType.GROUP if guest_group else HotelOrder.GuestType.INDIVIDUAL
        )

        if data["guest_type"] == HotelOrder.GuestType.GROUP:\
            # validate duplicate room
            busy_rooms = []
            for room in rooms:
                if room.is_busy:
                    busy_rooms.append(room)
            if busy_rooms:
                names = ", ".join([f"{room.hotel.name} - {room.room_number}" for room in busy_rooms])
                raise serializers.ValidationError(f"Quyidagi xonalar band: {names}")

        if guest_group and guests_data:
            raise CustomExceptionError(code=400, detail="Faqat bittasi: guest_group yoki guest_details")

        if not guest_group and not guests_data:
            raise CustomExceptionError(code=400, detail="guest_group yoki guest_details kerak")

        if guests_data and not room:
            raise CustomExceptionError(code=400, detail="Individual order uchun room shart")

        if guest_group and not rooms:
            raise CustomExceptionError(code=400, detail="Group order uchun rooms kerak")

        if guests_data and data.get("count_of_people") != len(guests_data):
            raise CustomExceptionError(code=400, detail="guest_details bilan count_of_people mos emas")

        # Extra validation: For GROUP orders make sure selected rooms have enough total capacity
        if guest_group and rooms:
            # rooms here is a list or queryset of Room instances (converted by DRF)
            total_capacity = 0
            for r in rooms:
                # Each Room represents a type with 'count' units, each with 'capacity'
                room_capacity_total = (getattr(r, "capacity", 0) or 0) * (getattr(r, "count", 0) or 0)
                total_capacity += room_capacity_total

            if count_of_people and total_capacity < count_of_people:
                raise CustomExceptionError(
                    code=400,
                    detail=f"Tanlangan xonalar sig'imi ({total_capacity}) kiritilgan odamlar sonidan ({count_of_people}) kam."
                )

        return data

    def create(self, validated_data):
        guests_data = validated_data.pop("guest_details", [])
        guest_group_id = validated_data.pop("guest_group", None)
        rooms = validated_data.pop("rooms", [])
        food_orders = validated_data.pop("food_order", [])
        count_of_people = validated_data.get("count_of_people") or 0


        with transaction.atomic():
            order = HotelOrder.objects.create(**validated_data)
            order.food_order.set(food_orders)
            guest_type = validated_data.get("guest_type")
            # Individual guest order
            if guests_data:
                guests = prepare_bulk_guests(
                    hotel=order.hotel,
                    room=order.room,
                    guests_data=guests_data,
                    check_in=order.check_in,
                    check_out=order.check_out
                )
                Guest.objects.bulk_create(guests)
                order.guests.set(guests)

            # Group guest order
            elif guest_group_id:
                order.guest_group_id = guest_group_id
                order.save(update_fields=["guest_group"])
                order.rooms.set(rooms)

                guest_group = GuestGroup.objects.get(id=guest_group_id)
                guest_group.guest_group_status = GuestGroup.GuestGroupStatus.ACCEPTED
                guest_group.save(update_fields=["guest_group_status"])


            # Price
            calculate_prices_for_order(order)
            order.save(update_fields=["general_cost"])

            # Room occupancy refresh
            rooms_to_refresh = (
                [order.room] if order.guest_type == HotelOrder.GuestType.INDIVIDUAL else rooms
            )
            for room in rooms_to_refresh:
                update_room_occupancy(room)

        return order

{
    "hotel": "53c020ff-48f4-447a-a760-5047fe436439",
    "order_status": "Active",
    "room": "0ada09a6-a2e2-4c78-adc4-878447122776",
    "guest_details": [
        {"full_name": "Gerakl", "gender": 1}
    ],
    "check_in": "19.10.2025 17:01",
    "check_out": "19.10.2025 17:03",
    "count_of_people": 1
}

{
    "hotel": "47e4e8a4-5672-4450-b8e6-f4f01f8806c7",
    "order_status": "Active",
    "rooms": [
     "b02b190a-c79f-45a0-aea1-fbc844a22e5d"
],
    "guest_group": "b1ce9272-fd4d-4964-84b6-c4cc46a46bea",
    "check_in": "18.10.2025 11:50",
    "check_out": "18.10.2025 11:52",
    "count_of_people": 2
}