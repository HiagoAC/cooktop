"""
Tests for the tags API.
"""

import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from app.utils_test import create_user, auth_header
from recipe.models import Tag

User = get_user_model()
TAGS_LIST_URL = reverse('api:tag_list')


class PublicPantryAPITests(TestCase):
    """Test unauthenticated requests to the tags API."""

    def setUp(self):
        self.client = Client()

    def test_unauthenticated_tag_list_request(self):
        """
        Test that retrieving tags list unauthenticated is
        unauthorized.
        """
        response = self.client.get(TAGS_LIST_URL)

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)


class PrivatePantryAPITests(TestCase):
    """Test authenticated requests for the tags api."""

    def setUp(self):
        self.user = create_user()
        self.headers = auth_header(self.user)
        self.client = Client()

    def test_retrieve_tag_list(self):
        """Test retrieving tags list added by any user."""
        tag_1 = Tag.objects.create(name='tag_1', added_by=self.user)
        tag_2 = Tag.objects.create(
            name='tag_2',
            added_by=create_user(email='another_user@example.com')
        )
        response = self.client.get(TAGS_LIST_URL, **self.headers)
        content = json.loads(response.content.decode('utf-8'))

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        expected = [
            {'id': tag_1.id, 'name': tag_1.name},
            {'id': tag_2.id, 'name': tag_2.name}
        ]
        self.assertEqual(content, expected)
