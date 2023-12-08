"""
Tests for user app validators.
"""

from user.validators import ContainDigitPasswordValidator

from django.test import TestCase
from django.core.exceptions import ValidationError


class ContainDigitPasswordValidatorTests(TestCase):
    """Test ContainDigitPasswordValidator."""

    def test_validate_success(self):
        """Test that no errors are raised if password contains a digit."""
        passwords = ['pass1wordd', '1passwordd', 'password12']
        validator = ContainDigitPasswordValidator()
        try:
            for password in passwords:
                validator.validate(password)
        except ValidationError:
            self.fail("ContainDigitPasswordValidator \
                        raised ValidationError unexpectedly.")

    def test_invalid_password_raise_error(self):
        """Test that a password with no digits raises ValidationError."""
        password = 'password'
        validator = ContainDigitPasswordValidator()
        with self.assertRaises(ValidationError):
            validator.validate(password)
