"""
User app models.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create a new user, save and return it."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractUser, PermissionsMixin):
    """User in the system."""
    # Required
    email = models.EmailField(max_length=255, unique=True)

    # Optional fields with default values
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Optional fields
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['']
