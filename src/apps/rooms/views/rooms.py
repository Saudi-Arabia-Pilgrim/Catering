from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.rooms.models import RoomType
from apps.rooms.serializers import RoomTypeSerializer


class RoomTypeListAPIView(CustomGenericAPIView):
    """
    API view to retrieve a list of all room types.

    This endpoint returns a list of all room types available in the system.

    Attributes:
        queryset (QuerySet): The queryset containing all RoomType instances.
        serializer_class (Serializer): The serializer used for room types.
    """

    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve the list of room types.

        Args:
            request (Request): The request object.

        Returns:
            Response: A response containing serialized room type data.
        """
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class RoomTypeCreateAPIView(CustomGenericAPIView):
    """
    API view to create a new room type.

    This endpoint allows users to add a new room type to the system.

    Attributes:
        queryset (QuerySet): The queryset containing all RoomType instances.
        serializer_class (Serializer): The serializer used for room types.
    """

    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new room type.

        Args:
            request (Request): The request object containing room type data.

        Returns:
            Response: A response containing the created room type data.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RoomTypeRetrieveAPIView(CustomGenericAPIView):
    """
    API view to retrieve details of a specific room type.

    This endpoint fetches and returns the details of a specific room type.

    Attributes:
        queryset (QuerySet): The queryset containing all RoomType instances.
        serializer_class (Serializer): The serializer used for room types.
    """

    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    def get(self, request, pk, *args, **kwargs):
        """
        Handles GET requests to retrieve a specific room type by ID.

        Args:
            request (Request): The request object.
            pk (int): The primary key of the room type to retrieve.

        Returns:
            Response: A response containing serialized room type data.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class RoomTypeUpdateAPIView(CustomGenericAPIView):
    """
    API view to update details of a specific room type.

    This endpoint allows users to update room type details either fully or partially.

    Attributes:
        queryset (QuerySet): The queryset containing all RoomType instances.
        serializer_class (Serializer): The serializer used for room types.
    """

    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    def get(self, request, pk, *args, **kwargs):
        """
        Handles GET requests to retrieve a specific room type by ID.

        Args:
            request (Request): The request object.
            pk (int): The primary key of the room type to retrieve.

        Returns:
            Response: A response containing serialized room type data.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def patch(self, request, pk, *args, **kwargs):
        """
        Handles PATCH requests to partially update a room type.

        Args:
            request (Request): The request object containing updated data.
            pk (int): The primary key of the room type to update.

        Returns:
            Response: A response containing updated room type data.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RoomTypeDeleteAPIView(CustomGenericAPIView):
    """
    API view to delete a specific room type.

    This endpoint allows users to delete an existing room type from the system.

    Attributes:
        queryset (QuerySet): The queryset containing all RoomType instances.
        serializer_class (Serializer): The serializer used for room types.
    """

    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    def get(self, request, pk, *args, **kwargs):
        """
        Handles GET requests to retrieve a specific room type before deletion.

        Args:
            request (Request): The request object.
            pk (int): The primary key of the room type to retrieve.

        Returns:
            Response: A response containing serialized room type data.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        """
        Handles DELETE requests to remove a specific room type.

        Args:
            request (Request): The request object.
            pk (int): The primary key of the room type to delete.

        Returns:
            Response: A response with a 204 status indicating successful deletion.
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=204)
