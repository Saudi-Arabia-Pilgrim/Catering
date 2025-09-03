from apps.base.permissions import RoleBasedPermission
from apps.users.models import CustomUser


class RoleBasedAccessMixin:
    """
    Mixin that adds role-based access control to a view.
    
    Usage:
    class MyView(RoleBasedAccessMixin, APIView):
        required_role = CustomUser.UserRole.HOTEL
        
        def get(self, request):
            # Only users with the HOTEL role can access this view
            return Response(...)
    """
    permission_classes = [RoleBasedPermission]
    required_role = None


class AdminAccessMixin(RoleBasedAccessMixin):
    """Mixin for views that should only be accessible by admins."""
    required_role = CustomUser.UserRole.ADMIN


class CEOAccessMixin(RoleBasedAccessMixin):
    """Mixin for views that should only be accessible by CEOs."""
    required_role = CustomUser.UserRole.CEO


class HRAccessMixin(RoleBasedAccessMixin):
    """Mixin for views that should only be accessible by HR."""
    required_role = CustomUser.UserRole.HR


class HotelAccessMixin(RoleBasedAccessMixin):
    """Mixin for views that should only be accessible by Hotel staff."""
    required_role = CustomUser.UserRole.HOTEL


class CateringAccessMixin(RoleBasedAccessMixin):
    """Mixin for views that should only be accessible by Catering staff."""
    required_role = CustomUser.UserRole.CATERING


class TransportationAccessMixin(RoleBasedAccessMixin):
    """Mixin for views that should only be accessible by Transportation staff."""
    required_role = CustomUser.UserRole.TRANSPORTATION


class AnalyticsAccessMixin(RoleBasedAccessMixin):
    """Mixin for views that should only be accessible by Analytics staff."""
    required_role = CustomUser.UserRole.ANALYTICS


class WarehouseAccessMixin(RoleBasedAccessMixin):
    """Mixin for views that should only be accessible by Warehouse staff."""
    required_role = CustomUser.UserRole.WAREHOUSE