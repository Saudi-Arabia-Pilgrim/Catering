from django.db import transaction

from rest_framework import serializers

from apps.rooms.models import Room
from apps.guests.models import Guest
from apps.base.exceptions import CustomExceptionError
from apps.orders.models.hotel_order import HotelOrder
from apps.base.serializers import CustomModelSerializer
from apps.orders.serializers import OnlyFoodOrderSerializer
from apps.guests.utils.prepare_guests import prepare_bulk_guests
from apps.guests.serializers.order_guests import GuestListSerializer


class HotelOrderGuestSerializer(CustomModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), required=False)
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
        return data

    def validate(self, data):
        count_of_people = data.get("count_of_people", 0)
        guests_data = data.get("guest_details", [])
        guest_group = data.get("guest_group", None)

        if guest_group and guests_data:
            raise CustomExceptionError(
                code=400,
                detail="Iltimos, yoki `guest_group`, yoki `guest_details` dan birini kiriting — ikkalasi birga bo‘lmaydi.")

        if not guest_group and not guests_data:
            raise CustomExceptionError(
                code=400,
                detail="Iltimos, `guest_group` yoki `guest_details` dan birini kiriting.")

        if guests_data and count_of_people != len(guests_data):
            raise CustomExceptionError(code=400, detail="Mehmonlar soni kiritilgan odamlar soniga teng bo‘lishi kerak.")

        return data

    def create(self, validated_data):
        guests_data = validated_data.pop("guest_details", [])
        guest_group_id = validated_data.pop("guest_group", None)
        rooms = validated_data.pop("rooms", [])  # M2M bo‘lsa, kerak bo‘ladi
        food_orders = validated_data.pop("food_order", [])

        with transaction.atomic():
            # Guest turi aniqlanadi
            if guest_group_id:
                validated_data["guest_type"] = HotelOrder.GuestType.GROUP
            elif guests_data:
                validated_data["guest_type"] = HotelOrder.GuestType.INDIVIDUAL
            else:
                raise CustomExceptionError(code=400, detail="Mehmonlar haqida ma'lumot yo‘q.")

            # Order yaratiladi (rooms, guests holda)
            hotel_order = HotelOrder.objects.create(**validated_data)

            # Food orders (M2M)
            hotel_order.food_order.set(food_orders)

            # === INDIVIDUAL ORDER ===
            if guests_data:
                guests = prepare_bulk_guests(
                    hotel=hotel_order.hotel,
                    room=hotel_order.room,
                    guests_data=guests_data,
                    check_in=hotel_order.check_in,
                    check_out=hotel_order.check_out
                )
                Guest.objects.bulk_create(guests)
                hotel_order.guests.set(guests)

            # === GROUP ORDER ===
            elif guest_group_id:
                hotel_order.guest_group_id = guest_group_id
                hotel_order.save(update_fields=["guest_group"])

                # Rooms ni bog‘lash (ManyToMany)
                hotel_order.rooms.set(rooms)

            # Narxlar hisoblanadi
            hotel_order.calculate_prices()
            hotel_order.save(update_fields=["general_cost"])

            # Occupancy yangilanadi
            if hotel_order.guest_type == HotelOrder.GuestType.INDIVIDUAL:
                hotel_order.room.refresh_occupancy()
            elif hotel_order.guest_type == HotelOrder.GuestType.GROUP:
                hotel_order.rooms.prefetch_related(None)  # remove prefetch if exists
                for room in hotel_order.rooms.all():  # Bu yerda bir martalik query ketadi
                    room.refresh_occupancy()

        return hotel_order


{
    "hotel": "5956b868-ff3c-4ab8-871f-6e74bebb44f4",
    "order_status": "Planned",
    "room": "56ee7e7d-a7ea-4c39-8c6a-89f12f69e194",
    "guest_details": [
        {"full_name": "Franko", "gender": 1}
    ],
    "check_in": "18.09.2025 15:50",
    "check_out": "25.09.2025 15:50",
    "count_of_people": 1
}

{
    "hotel": "7aa1b483-04a2-4d4d-b57f-ff7bfc0f4340",
    "order_status": "Active",
    "rooms": [
     "ecccc7e4-225b-4531-a40d-64f74d2db2ec",
     "43c8e031-1c7a-4b1c-a44c-b6acd367dd05",
     "5cc6210a-de71-4219-826e-53c796f044a9",
     "f069547b-52de-4c22-adb1-aab44ff43228",
     "2dfa94a0-1a32-4289-9b67-84297410aaa0"
],
    "guest_group": "07d73f63-11dd-4531-baba-2136cd061605",
    "check_in": "18.07.2025 15:50",
    "check_out": "25.07.2025 15:50",
    "count_of_people": 10
}
