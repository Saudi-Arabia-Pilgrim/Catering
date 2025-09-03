from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from apps.users.models import CustomUser


def setup_group_permissions(group, app_labels):
    """
    Set up permissions for a group based on app labels.
    :param group: Group instance
    :param app_labels: List of app labels to grant permissions for
    :return: None
    """
    # Clear existing permissions
    group.permissions.clear()

    # Add permissions for each app label
    for app_label in app_labels:
        content_types = ContentType.objects.filter(app_label=app_label)
        permissions = Permission.objects.filter(content_type__in=content_types)
        group.permissions.add(*permissions)


@receiver(post_save, sender=CustomUser)
def assign_user_to_group(sender, instance=None, created=False, **kwargs):
    """
    Assign users to default groups based on their role upon creation.

    This function assigns users to groups based on their role and sets up appropriate permissions.
    Each user role is granted full permissions for their department.
    """
    # Skip if this signal has been processed already (to avoid recursion)
    # This check is necessary because at the end of this function we call instance.save(),
    # which would trigger this signal again, creating an infinite loop.
    # The _skip_signal attribute is set to True before saving to break this loop.
    if instance._skip_signal:
        return

    # Remove user from all groups first (in case of role change)
    instance.groups.clear()

    # Determine the group based on the user's role
    if instance.is_superuser:
        group, _ = Group.objects.get_or_create(name='Superuser')
        # Superusers have access to everything
        setup_group_permissions(group, [
            'users', 'hotels', 'rooms', 'guests', 'orders', 'expenses', 'transports', 'authentication'
        ])
    elif instance.role == CustomUser.UserRole.ADMIN:
        group, _ = Group.objects.get_or_create(name='Administrators')
        setup_group_permissions(group, [
            'users', 'hotels', 'rooms', 'guests', 'orders', 'transports', 'authentication'
        ])
    elif instance.role == CustomUser.UserRole.CEO:
        group, _ = Group.objects.get_or_create(name='CEO')
        setup_group_permissions(group, [
            'users', 'hotels', 'rooms', 'guests', 'orders', 'expenses', 'transports', 'authentication'
        ])
    elif instance.role == CustomUser.UserRole.HR:
        group, _ = Group.objects.get_or_create(name='HR')
        setup_group_permissions(group, ['users'])
    elif instance.role == CustomUser.UserRole.HOTEL:
        group, _ = Group.objects.get_or_create(name='Hotel Team')
        setup_group_permissions(group, ['hotels', 'rooms', 'guests'])
    elif instance.role == CustomUser.UserRole.CATERING:
        group, _ = Group.objects.get_or_create(name='Catering Team')
        setup_group_permissions(group, ['orders'])
    elif instance.role == CustomUser.UserRole.TRANSPORTATION:
        group, _ = Group.objects.get_or_create(name='Transportation Team')
        setup_group_permissions(group, ['transports'])
    elif instance.role == CustomUser.UserRole.ANALYTICS:
        group, _ = Group.objects.get_or_create(name='Analytics Team')
        setup_group_permissions(group, ['hotels', 'rooms', 'guests', 'orders', 'expenses', 'transports'])
    elif instance.role == CustomUser.UserRole.WAREHOUSE:
        group, _ = Group.objects.get_or_create(name='Warehouse Team')
        setup_group_permissions(group, ['orders'])
    else:
        # If no matching role is found, exit without making changes
        return

    # Add the user to the selected group
    instance.groups.add(group)

    # Mark that the signal has been processed to avoid recursion
    instance._skip_signal = True
    instance.save()

    # Reset the flag after saving
    instance._skip_signal = False
