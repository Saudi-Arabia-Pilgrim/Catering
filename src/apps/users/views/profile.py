from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.users.filters import EmployeeFilter
from apps.users.serializers.custom_user import UserProfileSerializer


class UserProfileAPIView(CustomGenericAPIView):
    """
    API view for user profile management.
    Allows users to view and update their profile information.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = EmployeeFilter
    search_fields = ["email", "full_name", "phone_number", "passport_number", "role", "gender", "base_salary"]

    def get(self, request):
        """
        Retrieve the user's profile information.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Update the user's profile information.
        """
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """
        Partially update the user's profile information.
        """
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)