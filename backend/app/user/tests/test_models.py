"""
Tests for user app models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
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
        
    def test_user_str_representation(self):
        """Test __str__ method of user."""
        pass