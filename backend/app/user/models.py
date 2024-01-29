"""
User app models.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.password_validation import validate_password


class UserManager(BaseUserManager):
    """Manager for users."""
    def create_superuser(self, email, password=None, **extra_fields):
        """Create a superuser, save and return it."""
        superuser = self.create_user(email, password, **extra_fields)
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save(using=self._db)

        return superuser

    def create_user(self, email, password=None, **extra_fields):
        """Create a new user, save and return it."""
        if not email:
            raise ValueError('The Email field must be set')

        # Normalizes address: email@EXAMPLE.com -> email@example.com
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        # Raise ValidationError if password is invalid
        # It uses AUTH_PASSWORD_VALIDATORS defined in settings
        validate_password(password)

        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User in the system.

    Required fields: email, password
    Other fields are optional.
    """
    # Required field
    email = models.EmailField(max_length=255, unique=True)

    # Optional fields
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    # Optional fields with default values
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_fullname(self):
        """
        Return a string with user's full name.

        If both names are not set it returns the user's email.
        """
        if self.first_name == '' and self.last_name == '':
            return self.email
        elif self.first_name == '':
            return self.last_name
        elif self.last_name == '':
            return self.first_name
        else:
            return f'{self.first_name} {self.last_name}'


class RefreshToken(models.Model):
    """Last refresh token of each user."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='refresh_token'
    )
    refresh_token = models.CharField(max_length=255, unique=True)
