from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager

from config import settings

User = settings.AUTH_USER_MODEL

class CustomUserManager(UserManager):
    """
    Custom user model manager where email is the unique identifier
    """
    def _create_user(self, email, password, **extra_fields) -> User: # type: ignore
        """
        Create and save a User with the given (email) and password.
        :param email: User's email address
        :param password: User's password
        :param extra_fields: Additional fields
        :return: User instance
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email=email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields) -> User: # type: ignore
        """
        Creates and saves a new user
        :param email: User's email address.
        :param password: User's password
        :param extra_fields: Additional fields
        :return: User instance
        """
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields) -> User: # type: ignore
        """
        Creates and saves a new superuser
        :param email: User's email address
        :param password: User's password
        :param extra_fields: Additional fields
        :return: User instance
        """
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
