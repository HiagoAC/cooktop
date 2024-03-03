"""
Tests for the preferences API.
"""

import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from app.utils_test import create_user, auth_header
from meal_plan.models import Preferences

User = get_user_model()
PREFERENCES_URL = reverse('api:preferences')


class PublicPreferencesAPITests(TestCase):
    """Test unauthenticated requests to the preferences API."""

    def setUp(self):
        self.client = Client()

    def test_unauthenticated_get_preferences_request(self):
        """
        Test that retrieving preferences unauthenticated is
        unauthorized.
        """
        response = self.client.get(PREFERENCES_URL)

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)


class PrivatePreferencesAPITests(TestCase):
    """Test authenticated requests for the preferences API."""

    def setUp(self):
        self.user = create_user()
        self.headers = auth_header(self.user)
        self.client = Client()

    def test_get_preferences(self):
        """Test getting user's meal plan preferences."""
        preferences = Preferences.objects.create(
            user=self.user,
            servings_per_meal=4,
            cookings_per_week=6,
            )
        response = self.client.get(PREFERENCES_URL, **self.headers)
        content = json.loads(response.content.decode('utf-8'))

        # 200 - OK
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            content['servings_per_meal'], preferences.servings_per_meal)
        self.assertEqual(
            content['cookings_per_week'], preferences.cookings_per_week)

    def test_set_preferecens(self):
        """Test setting meal plan preferences."""
        payload = {
            'servings_per_meal': 4,
            'cookings_per_week': 6,
        }
        response = self.client.post(
            PREFERENCES_URL,
            data=json.dumps(payload),
            content_type='application/json',
            **self.headers
        )
        content = json.loads(response.content.decode('utf-8'))

        # 201 - CREATED
        self.assertEqual(response.status_code, 201)
        for field, value in payload.items():
            self.assertEqual(content[field], value)

    def test_update_preferences(self):
        """Test updating meal plan preferences."""
        preferences = Preferences.objects.create(
            user=self.user,
            servings_per_meal=4,
            cookings_per_week=6,
            )
        new_data = {
            'servings_per_meal': 5,
            'cookings_per_week': 5,
        }
        response = self.client.patch(
            PREFERENCES_URL,
            data=json.dumps(new_data),
            content_type='application/json',
            **self.headers,
        )
        preferences.refresh_from_db()

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        for attr, value in new_data.items():
            self.assertEqual(value, getattr(preferences, attr))
