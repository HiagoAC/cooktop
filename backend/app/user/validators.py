"""
Custom password validators.
"""

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class ContainDigitPasswordValidator:
    """
    Validate that the password is not entirely letters.
    """

    def validate(self, password, user=None):
        if not any(c.isdigit() for c in password):
            raise ValidationError(
                _("This password does not contain any digits."),
                code="password_no_digits",
            )

    def get_help_text(self):
        return _("Your password must contain at least one digit.")
