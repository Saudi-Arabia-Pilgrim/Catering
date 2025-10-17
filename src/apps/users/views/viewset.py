from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.contrib.auth import get_user_model

from apps.base.views import CustomModelViewSet
from apps.users.serializers import UserSerializer
from apps.users.permissions import RoleBasedPermission
from apps.users.filters import EmployeeFilter


class UserViewSet(CustomModelViewSet):
    queryset = get_user_model().objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    filterset_class = EmployeeFilter
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["full_name", "email", "phone_number", "passport_number"]
    department = 'hr'

    def get_permissions(self):
        """
        Use both IsAuthenticated and RoleBasedPermission for permission checking.
        :return:
        """
        permission_classes = [IsAuthenticated, RoleBasedPermission]
        return [permission() for permission in permission_classes]

    def get_object(self):
        """
        If the action is 'me', return the current user.
        Otherwise, use the default behavior.
        """
        if self.action == 'me':
            return self.request.user
        return super().get_object()

    def get_queryset(self):
        """
        Filter the queryset based on the user's role.
        Superusers and admins can see all users.
        Other users can only see themselves.
        """
        # Check if this is a schema generation request
        if getattr(self, 'swagger_fake_view', False):
            # Return an empty queryset for schema generation
            return self.queryset.none()

        user = self.request.user
        # Check if user is authenticated and has necessary attributes
        if not user.is_authenticated:
            return self.queryset.none()

        if user.is_superuser or getattr(user, 'role', '') in ('ceo', 'hr', 'admin'):
            return self.queryset
        return self.queryset.filter(id=user.id)
