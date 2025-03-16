from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager

from config import settings

User = settings.AUTH_USER_MODEL

class CustomUserManager(UserManager):
    """
    Custom user model manager where email is the unique identifier
    """
    def _create_user(self, username, password, **extra_fields) -> User: # type: ignore
        """
        Create and save a User with the given username (email) and password.
        :param username: User's email address stored in username field
        :param password: User's password
        :param extra_fields: Additional fields
        :return: User instance
        """
        if not username:
            raise ValueError('The Email field must be set')
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, **extra_fields) -> User: # type: ignore
        """
        Creates and saves a new user
        :param username: User's email address stored in username field
        :param password: User's password
        :param extra_fields: Additional fields
        :return: User instance
        """
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username=None, password=None, **extra_fields) -> User: # type: ignore
        """
        Creates and saves a new superuser
        :param username: User's email address stored in username field
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

        return self._create_user(username, password, **extra_fields)
