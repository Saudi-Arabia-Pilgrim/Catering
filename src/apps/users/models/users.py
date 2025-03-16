from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.exceptions import CustomExceptionError
from apps.base.models import AbstractBaseModel
from apps.users.utils import CustomUserManager, validate_gmail


class CustomUser(AbstractBaseModel, AbstractBaseUser, PermissionsMixin):
    """
    A custom User model that implements fully featured User management with
    admin-compliant permissions.

    User email and password are required. Other fields are optional.
    Email is used as the main login identifier.
    """

    EMAIL_FIELD = 'username'
    USERNAME_FIELD = 'username'  # Using username field to store email
    REQUIRED_FIELDS = ['full_name']

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

    # Email is now the main identifier
    username = models.EmailField(_('Email address'), max_length=150, unique=True, validators=[validate_gmail])
    full_name = models.CharField(_('Full name'), max_length=150)

    # New fields
    birthdate = models.DateField(_('Birth date'), null=True, blank=True)
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

    # Additional fields as per requirements
    date_come = models.DateField(_('Date come'), null=True, blank=True)
    from_come = models.CharField(_('From come'), max_length=255, null=True, blank=True)
    passport_number = models.CharField(_('Passport number'), max_length=50, null=True, blank=True)
    given_by = models.CharField(_('Given by'), max_length=255, null=True, blank=True)
    validity_period = models.DateTimeField(_('Validity period'), null=True, blank=True)
    expenses = models.DecimalField(_('Expenses'), max_digits=10, decimal_places=2, null=True, blank=True)
    monthly_salary = models.DecimalField(_('Monthly salary'), max_digits=10, decimal_places=2, null=True, blank=True)
    general_expenses = models.DecimalField(_('General expenses'), max_digits=10, decimal_places=2, null=True, blank=True)

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
        Check username (which stores email)
        :return:
        """
        if not self.username:
            raise CustomExceptionError(code=400, detail='Email is required')


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
        send_mail(subject, message, from_email, [self.username], **kwargs)

    def __str__(self):
        return self.username
