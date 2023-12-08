"""
Tests for user app models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class UserModelTests(TestCase):
    """Test user app models."""

    def test_create_user(self):
        """Test creating user with required fields (email, password) is
        successful."""
        email = 'test@example.com'
        password = 'password321'

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_without_email(self):
        """Test creating user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='',
                password='password321'
            )

    def test_create_user_invalid_password(self):
        """Test setting invalid passwords raise ValidationError."""
        invalid_passwords = ['tooShort9',
                             '987653420470928']

        for password in invalid_passwords:
            with self.assertRaises(ValidationError):
                get_user_model().objects.create_user(
                    email='test@example.com',
                    password=password
                )

    def test_user_fields_defaults(self):
        """Test if user fields' defaults values are defined correctly."""
        email = 'test@example.com'
        password = 'password321'

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')

    def test_user_email_normalization(self):
        """Test email addresses are converted to lowercase to avoid duplicates
        of the same address."""
        email = 'tEst@EXAMPLE.com'
        password = 'password321'

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, 'tEst@example.com')

    def test_create_superuser(self):
        """Test creating superuser is successful."""
        email = 'test@example.com'
        password = 'password321'

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)

    def test_get_fullname(self):
        """Test getting a user full name."""
        email = 'test@example.com'
        first = 'John'
        last = 'Doe'
        user = get_user_model().objects.create_superuser(
            email=email,
            password='password321',
        )

        # User has no name
        name = user.get_fullname()
        self.assertEqual(name, email)

        # User only has first name
        user.first_name = first
        name = user.get_fullname()
        self.assertEqual(name, first)

        # User only has last name
        user.first_name = ''
        user.last_name = last
        name = user.get_fullname()
        self.assertEqual(name, last)

        # User has first and last name
        user.first_name = first
        name = user.get_fullname()
        self.assertEqual(name, f'{first} {last}')
