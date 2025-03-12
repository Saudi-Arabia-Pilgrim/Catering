from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.exceptions import CustomExceptionError
from apps.base.models import AbstractBaseModel
from apps.users.utils import CustomUserManager



class CustomUser(AbstractBaseModel, AbstractBaseUser, PermissionsMixin):
    """
    A custom User model that implements fully featured User management with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fullname', "email"]

    objects = CustomUserManager()

    username = models.CharField(_('username'), max_length=150, unique=True, blank=True)
    fullname = models.CharField(_('fullname'), max_length=150)

    email = models.EmailField(_('email'), unique=True, blank=True, null=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'), default=True, help_text=_(
            'Designates whether this user should be treated as active.'
            'Unselect this instead of deleting accounts.'
        ),
    )

    def clean(self):
        """
        Check email or phone number
        :return:
        """
        if not self.email and not self.username:
            raise CustomExceptionError(code=400, detail='Email or Username is required')


    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Email this User.
        :param subject:
        :param message:
        :param from_email:
        :param kwargs:
        :return:
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.username