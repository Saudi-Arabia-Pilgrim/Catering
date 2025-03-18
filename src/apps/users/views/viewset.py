from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from apps.base.views import CustomModelViewSet
from apps.users.serializers import UserSerializer
from apps.users.permissions import RoleBasedPermission


class UserViewSet(CustomModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    department = 'users'  # This is used by RoleBasedPermission

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

        if user.is_superuser or getattr(user, 'role', '') == 'admin':
            return self.queryset
        return self.queryset.filter(id=user.id)
