from django.db import models
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from apps.base.validators import validate_image_size
from apps.users.tasks import send_email_to_user
from apps.base.models import AbstractBaseModel
from apps.base.exceptions import CustomExceptionError
from apps.users.utils import CustomUserManager


class CustomUser(AbstractBaseModel, AbstractBaseUser, PermissionsMixin):
    """
    A custom User model that implements fully featured User management with
    admin-compliant permissions.

    User email and password are required. Other fields are optional.
    Email is used as the main login identifier.
    """

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    # Flag to prevent permission signals' recursion
    _skip_signal = False

    class UserRole(models.TextChoices):
        """
        User roles based on the department, such as Admin, CEO, HR, Hotel, Catering, Transportation, Analytics, and Warehouse.
        The full write/update/delete permissions are granted to each user role in vicinity to his/her department.
        """
        ADMIN = 'admin', _('Admin')
        CEO = 'ceo', _('CEO')
        HR = 'hr', _('HR')
        HOTEL = 'hotel', _('Hotel')
        CATERING = 'catering', _('Catering')
        TRANSPORTATION = 'transportation', _('Transportation')
        ANALYTICS = 'analytics', _('Analytics')
        WAREHOUSE = 'warehouse', _('Warehouse')

    class Gender(models.TextChoices):
        """
        Gender choices for the user.
        """
        MALE = 'male', _('Male')
        FEMALE = 'female', _('Female')

    objects = CustomUserManager()

    # === Biography ===
    full_name = models.CharField(_('Full name'), max_length=150)
    birthdate = models.DateField(_('Birth date'), null=True, blank=True)
    date_come = models.DateField(_('Date come'), null=True, blank=True)
    from_come = models.CharField(_('From come'), max_length=255, null=True, blank=True)

    # === Passport Info ===
    passport_number = models.CharField(_('Passport number'), max_length=50, null=True, blank=True)
    given_by = models.CharField(_('Given by'), max_length=255, null=True, blank=True)
    validity_period = models.DateTimeField(_('Passport Validity period'), null=True, blank=True)

    # Email is now the main identifier
    email = models.EmailField(
        _('Email address'),
        max_length=150,
        unique=True
    )
    phone_number = models.CharField(
        _("Phone Number"),
        max_length=15,
        null=True,
        blank=True,
        help_text=_("Employee's phone number if exists")
    )
    image = models.ImageField(
        _('Image'),
        upload_to='users/',
        validators=[validate_image_size],
        null=True,
        blank=True,
        help_text=_('Upload a profile image. Max size: 5MB')
    )
    gender = models.CharField(
        _('Gender'),
        max_length=10,
        choices=Gender.choices,
        null=True,
        blank=True
    )
    # Role field to store the user's department
    role = models.CharField(
        _('Role'),
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.ADMIN,
        help_text=_('Designates the department this user belongs to and their permissions.')
    )
    total_expenses = models.DecimalField(
        _('Total Expenses'),
        max_digits=10,
        decimal_places=2,
        default=0.00,
        null=True,
        blank=True,
        help_text=_('Total expenses for visa sponsoring, plane tickets, etc. (in USD)')
    )
    base_salary = models.DecimalField(
        _('Base Salary'),
        max_digits=10,
        decimal_places=2,
        default=0.00,
        null=True,
        blank=True,
        help_text=_('Monthly base salary amount (in USD)')
    )
    total_general_expenses = models.DecimalField(
        _('General expenses'), 
        max_digits=10, 
        decimal_places=2,
        default=0.00,
        null=True, 
        blank=True,
        help_text=_('Expenses for accommodation, rent, etc. (in USD)')
    )
    is_staff = models.BooleanField(
        _('Staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active.'
            'Unselect this instead of deleting accounts.'
        ),
    )

    def clean(self):
        """
        Check email.
        :return: CustomExceptionError
        """
        try:
            super().clean()
        except Exception as e:
            raise CustomExceptionError(code=400, detail=str(e))

    @classmethod
    def revoke_user_tokens(cls, user):
        """
        Revoke all tokens for the user.
        """
        token_strings = OutstandingToken.objects.filter(user_id=user.id).values_list('token', flat=True)
        try:
            for token_string in token_strings:
                refresh_token = RefreshToken(token_string)
                refresh_token.blacklist()
        except Exception as e:
            pass

    @staticmethod
    def email_user(self, subject: str, message: str):
        """
        Easily send an email this current user on the go!
        :param self: User
        :param subject: The subject/title of the email.
        :param message: The message to be sent.
        :return:
        """
        send_email_to_user(subject=subject,  email=self.email, message=message)


    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')


    def __str__(self):
        return self.email
