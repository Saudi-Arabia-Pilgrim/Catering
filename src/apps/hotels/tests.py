# class HotelListAPIView(CustomGenericAPIView):
#     """
#     API view to retrieve a list of hotels.
#
#     This view fetches all hotels from the database and returns their serialized data.
#     """
#     queryset = Hotel.objects.prefetch_related(
#         Prefetch(
#             "rooms",
#             queryset=Room.objects.select_related("room_type")
#             .only(
#                 'id', 'room_type__name', 'gross_price', 'occupied_count',
#                 'count', 'hotel_id', 'room_type_id', 'capacity', 'net_price'
#             )
#         ),
#         Prefetch(
#             "guests",
#             queryset=Guest.objects.select_related('room', 'room__room_type')
#             .only(
#                 'id', 'full_name', 'order_number', 'room_id',
#                 'gender', 'check_in', 'check_out', 'hotel_id'
#             )
#         )HotelListAPIView
#     ).all()
#     serializer_class = HotelSerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     filterset_class = RoomWithGuestFilter
#     search_fields = ["name__icontains"]
#
#     def get(self, *args, **kwargs):
#         """
#         Handle GET requests to return the list of hotels.
#
#         Returns:
#             Response: A response containing the serialized list of hotels.
#         """
#         queryset = self.filter_queryset(self.get_queryset())
#
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)










# ========================================

# class HotelListAPIView(CustomGenericAPIView):
#     """
#     API view to retrieve a list of hotels filtered by room type name.
#     """
#
#     serializer_class = HotelSerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     filterset_class = RoomWithGuestFilter
#     search_fields = ["name__icontains"]
#
#     def get_queryset(self):
#         room_type_name = self.request.query_params.get("room_type_name")
#
#         # Filter Guests
#         guest_qs = Guest.objects.select_related('room', 'room__room_type').only(
#             'id', 'full_name', 'order_number', 'room_id',
#             'gender', 'check_in', 'check_out', 'hotel_id'
#         )
#         if room_type_name:
#             guest_qs = guest_qs.filter(room__room_type__name__icontains=room_type_name)
#
#         # Filter Rooms
#         room_qs = Room.objects.select_related("room_type").only(
#             'id', 'room_type__name', 'gross_price', 'occupied_count',
#             'count', 'hotel_id', 'room_type_id', 'capacity', 'net_price'
#         )
#         if room_type_name:
#             room_qs = room_qs.filter(room_type__name__icontains=room_type_name)
#
#         # Filter Hotels with only matching rooms
#         hotels_qs = Hotel.objects.prefetch_related(
#             Prefetch("rooms", queryset=room_qs),
#             Prefetch("guests", queryset=guest_qs)
#         )
#         if room_type_name:
#             hotels_qs = hotels_qs.filter(rooms__room_type__name__icontains=room_type_name).distinct()
#
#         return hotels_qs
#
#     def get(self, *args, **kwargs):
#         """
#         Handle GET requests to return the list of hotels.
#         """
#         queryset = self.filter_queryset(self.get_queryset())
#
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)