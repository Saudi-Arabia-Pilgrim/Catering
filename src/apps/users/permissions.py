from rest_framework import permissions
from apps.users.models import CustomUser

class RoleBasedPermission(permissions.BasePermission):
    """
    Permission class that restricts users to only access data related to their department.
    """
    
    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.
        """
        # Superusers and admins have full access
        if request.user.is_superuser or request.user.role == CustomUser.UserRole.ADMIN:
            return True
            
        # Check if the view has a department attribute
        if hasattr(view, 'department'):
            # Check if the user's role matches the view's department
            return request.user.role == view.department
            
        # If the view doesn't specify a department, allow access
        return True
        
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the object.
        """
        # Superusers and admins have full access
        if request.user.is_superuser or request.user.role == CustomUser.UserRole.ADMIN:
            return True
            
        # Check if the object has a department attribute
        if hasattr(obj, 'department'):
            # Check if the user's role matches the object's department
            return request.user.role == obj.department
            
        # If the object doesn't have a department attribute, check if it has a user attribute
        if hasattr(obj, 'user'):
            # Allow access if the user is the owner
            return obj.user == request.user
            
        # If the object doesn't have a department or user attribute, allow access
        return True