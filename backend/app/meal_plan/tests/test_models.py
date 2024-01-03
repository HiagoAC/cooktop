"""Tests for models in the meal_plan app."""

from django.test import TestCase

from app.utils_test import create_user
from meal_plan.models import Preferences


class PreferencesModelTests(TestCase):
    """Tests for the Preferences model."""

    def test_create_preferences(self):
        """Test creating a preferences object."""
        params = {
            'user': create_user(),
            'servings_per_week': 14,
            'cookings_per_week': 7,
        }
        prefs = Preferences.objects.create(**params)

        for attr, value in params.items():
            self.assertEqual(getattr(prefs, attr), value)
