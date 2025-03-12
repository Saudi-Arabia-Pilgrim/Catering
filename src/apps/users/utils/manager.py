from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager

from config import settings

User = settings.AUTH_USER_MODEL

class CustomUserManager(UserManager):
    """
    Custom user model manager where email is the unique identifiers
    """
    def _create_user(self, username, email, password, **extra_fields) -> User: # type: ignore
        """
        Create and save a User with the given username, email and password.
        :param username:
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, **extra_fields) -> User: # type: ignore
        """
        Creates and saves a new user
        :param extra_fields:
        :return:
        """
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        return self._create_user(**extra_fields)

    def create_superuser(self, **extra_fields) -> User: # type: ignore
        """
        Creates and saves a new superuser
        :param extra_fields:
        :return:
        """
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(**extra_fields)


