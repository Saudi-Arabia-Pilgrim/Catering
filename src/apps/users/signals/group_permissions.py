from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import CustomUser


@receiver(post_save, sender=CustomUser)
def assign_user_to_group(sender, instance=None, created=False, **kwargs):
    """
    Assign users to default groups based on their role upon creation.
    :param sender: CustomUser model
    :param instance: Instance of CustomUser model
    :param created: Boolean
    :param kwargs:
    :return:

     Permissions need to be manually added to the groups via the admin or another mechanism.
     Typically, you would define them in a data migration or manually in the admin.
    """
    if created:
        if instance.is_superuser:
            group, _ = Group.objects.get_or_create(name='Superuser')  # will have access even to finance.
        elif instance.username.startswith('admin_'):
            group, _ = Group.objects.get_or_create(name='Administrators')  # won't have access to reports.
        elif instance.username.startswith('catering_'):
            group, _ = Group.objects.get_or_create(name='Catering Team')
        elif instance.username.startswith('finance_'):
            group, _ = Group.objects.get_or_create(name='Finance Team')
        elif instance.username.startswith('hotel_'):
            group, _ = Group.objects.get_or_create(name='Hotel Team')

        else:
            return
        instance.groups.add(group)
        instance.save()