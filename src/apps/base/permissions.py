from rest_framework import permissions
from apps.users.models import CustomUser


class RoleBasedPermission(permissions.BasePermission):
    """
    Permission class that checks if a user has the appropriate role to access a resource.
    """
    
    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.
        """
        # Superusers have all permissions
        if request.user.is_superuser:
            return True
            
        # Check if the view has a required_role attribute
        required_role = getattr(view, 'required_role', None)
        if required_role is None:
            # If no required_role is specified, fall back to default permission logic
            return True
            
        # Check if the user has the required role
        return request.user.role == required_role
        
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the object.
        """
        # Superusers have all permissions
        if request.user.is_superuser:
            return True
            
        # Check if the view has a required_role attribute
        required_role = getattr(view, 'required_role', None)
        if required_role is None:
            # If no required_role is specified, fall back to default permission logic
            return True
            
        # Check if the user has the required role
        if request.user.role != required_role:
            return False
            
        # Check if the object has a department attribute that matches the user's role
        # This is a common pattern, but you might need to customize this based on your models
        department = getattr(obj, 'department', None)
        if department is not None:
            return str(department).lower() == request.user.role.lower()
            
        # If the object doesn't have a department attribute, check for other common patterns
        # For example, if the object has a 'role' attribute
        obj_role = getattr(obj, 'role', None)
        if obj_role is not None:
            return str(obj_role).lower() == request.user.role.lower()
            
        # If we can't determine the object's department, allow access
        # You might want to be more restrictive here depending on your requirements
        return True