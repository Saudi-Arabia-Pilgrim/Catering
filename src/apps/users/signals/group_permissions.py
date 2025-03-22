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
    for app_label in app_labels:from django.contrib.auth.models import Group, Permission
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
    :param sender: CustomUser model
    :param instance: Instance of CustomUser model
    :param created: Boolean
    :param kwargs:
    :return:

    This function assigns users to groups based on their role and sets up appropriate permissions.
    Each user role is granted full permissions for their department.
    """
    # Skip if this is called from within this function to avoid recursion
    if hasattr(instance, '_skip_signal') and instance._skip_signal:
        return

    # If the user is being created or updated
    # Remove user from all groups first (in case of role change)
    instance.groups.clear()

    # Assign to appropriate group based on role
    if instance.is_superuser:
        group, _ = Group.objects.get_or_create(name='Superuser')
        # Superusers have access to everything
        setup_group_permissions(group, ['users', 'hotels', 'rooms', 'guests', 'orders', 'expenses', 'transports', 'authentication'])
    elif instance.role == CustomUser.UserRole.ADMIN:
        group, _ = Group.objects.get_or_create(name='Administrators')
        # Admins have access to most things except sensitive financial data
        setup_group_permissions(group, ['users', 'hotels', 'rooms', 'guests', 'orders', 'transports', 'authentication'])
    elif instance.role == CustomUser.UserRole.CEO:
        group, _ = Group.objects.get_or_create(name='CEO')
        # CEOs have access to everything
        setup_group_permissions(group, ['users', 'hotels', 'rooms', 'guests', 'orders', 'expenses', 'transports', 'authentication'])
    elif instance.role == CustomUser.UserRole.HR:
        group, _ = Group.objects.get_or_create(name='HR')
        # HR has access to user data
        setup_group_permissions(group, ['users'])
    elif instance.role == CustomUser.UserRole.HOTEL:
        group, _ = Group.objects.get_or_create(name='Hotel Team')
        # Hotel team has access to hotel, room, and guest data
        setup_group_permissions(group, ['hotels', 'rooms', 'guests'])
    elif instance.role == CustomUser.UserRole.CATERING:
        group, _ = Group.objects.get_or_create(name='Catering Team')
        # Catering team has access to order data
        setup_group_permissions(group, ['orders'])
    elif instance.role == CustomUser.UserRole.TRANSPORTATION:
        group, _ = Group.objects.get_or_create(name='Transportation Team')
        # Transportation team has access to transport data
        setup_group_permissions(group, ['transports'])
    elif instance.role == CustomUser.UserRole.ANALYTICS:
        group, _ = Group.objects.get_or_create(name='Analytics Team')
        # Analytics team has read-only access to most data
        setup_group_permissions(group, ['hotels', 'rooms', 'guests', 'orders', 'expenses', 'transports'])
    elif instance.role == CustomUser.UserRole.WAREHOUSE:
        group, _ = Group.objects.get_or_create(name='Warehouse Team')
        # Warehouse team has access to inventory data
        setup_group_permissions(group, ['orders'])
    else:
        return

    instance.groups.add(group)

    # Avoid recursive save
    instance._skip_signal = True
    instance.save()

    content_types = ContentType.objects.filter(app_label=app_label)
    permissions = Permission.objects.filter(content_type__in=content_types)
    group.permissions.add(*permissions)


@receiver(post_save, sender=CustomUser)
def assign_user_to_group(sender, instance=None, created=False, **kwargs):
    """
    Assign users to default groups based on their role upon creation.
    :param sender: CustomUser model
    :param instance: Instance of CustomUser model
    :param created: Boolean
    :param kwargs:
    :return:

    This function assigns users to groups based on their role and sets up appropriate permissions.
    Each user role is granted full permissions for their department.
    """
    # Skip if this is called from within this function to avoid recursion
    if hasattr(instance, '_skip_signal') and instance._skip_signal:
        return

    # If the user is being created or updated
    # Remove user from all groups first (in case of role change)
    instance.groups.clear()

    # Assign to appropriate group based on role
    if instance.is_superuser:
        group, _ = Group.objects.get_or_create(name='Superuser')
        # Superusers have access to everything
        setup_group_permissions(group, ['users', 'hotels', 'rooms', 'guests', 'orders', 'expenses', 'transports', 'authentication'])
    elif instance.role == CustomUser.UserRole.ADMIN:
        group, _ = Group.objects.get_or_create(name='Administrators')
        # Admins have access to most things except sensitive financial data
        setup_group_permissions(group, ['users', 'hotels', 'rooms', 'guests', 'orders', 'transports', 'authentication'])
    elif instance.role == CustomUser.UserRole.CEO:
        group, _ = Group.objects.get_or_create(name='CEO')
        # CEOs have access to everything
        setup_group_permissions(group, ['users', 'hotels', 'rooms', 'guests', 'orders', 'expenses', 'transports', 'authentication'])
    elif instance.role == CustomUser.UserRole.HR:
        group, _ = Group.objects.get_or_create(name='HR')
        # HR has access to user data
        setup_group_permissions(group, ['users'])
    elif instance.role == CustomUser.UserRole.HOTEL:
        group, _ = Group.objects.get_or_create(name='Hotel Team')
        # Hotel team has access to hotel, room, and guest data
        setup_group_permissions(group, ['hotels', 'rooms', 'guests'])
    elif instance.role == CustomUser.UserRole.CATERING:
        group, _ = Group.objects.get_or_create(name='Catering Team')
        # Catering team has access to order data
        setup_group_permissions(group, ['orders'])
    elif instance.role == CustomUser.UserRole.TRANSPORTATION:
        group, _ = Group.objects.get_or_create(name='Transportation Team')
        # Transportation team has access to transport data
        setup_group_permissions(group, ['transports'])
    elif instance.role == CustomUser.UserRole.ANALYTICS:
        group, _ = Group.objects.get_or_create(name='Analytics Team')
        # Analytics team has read-only access to most data
        setup_group_permissions(group, ['hotels', 'rooms', 'guests', 'orders', 'expenses', 'transports'])
    elif instance.role == CustomUser.UserRole.WAREHOUSE:
        group, _ = Group.objects.get_or_create(name='Warehouse Team')
        # Warehouse team has access to inventory data
        setup_group_permissions(group, ['orders'])
    else:
        return

    instance.groups.add(group)

    # Avoid recursive save
    instance._skip_signal = True
    instance.save()
