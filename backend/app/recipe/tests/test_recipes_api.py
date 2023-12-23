"""
Tests for the recipes API.
"""

import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from app.utils_test import create_user, auth_header
from recipe.models import Recipe, Tag

User = get_user_model()
RECIPE_URL = reverse('api:recipes')


class PublicRecipesAPITests(TestCase):
    """Test unauthenticated requests to the recipes API."""

    def setUp(self):
        self.client = Client()

    def test_unauthenticated_recipe_list_request(self):
        """
        Test that retrieving recipes list unauthenticated is
        unauthorized.
        """
        response = self.client.get(RECIPE_URL)

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)


class PrivateRecipesAPITests(TestCase):
    """Test authenticated requests for the recipes api."""

    def setUp(self):
        self.user = create_user()
        self.headers = auth_header(self.user)
        self.client = Client()

    def test_retrieve_recipe_list(self):
        """Test retrieving recipes list authenticated."""
        recipe_1 = Recipe.objects.create(
            user=self.user,
            title='a recipe',
            directions=['step 1', 'step 2']
        )
        recipe_2 = Recipe.objects.create(
            user=self.user,
            title='a recipe',
            directions=['step 1', 'step 2']
        )
        response = self.client.get(RECIPE_URL, **self.headers)
        content = json.loads(response.content.decode('utf-8'))

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        expected = [
            {'id': recipe_1.id, 'title': recipe_1.title},
            {'id': recipe_2.id, 'title': recipe_2.title}
        ]
        self.assertEqual(content, expected)

    def test_retrieve_recipe_list_another_user(self):
        """Test retrieving recipes list authenticated."""
        recipe_1 = Recipe.objects.create(
            user=self.user,
            title='a recipe',
            directions=['step 1', 'step 2']
        )
        Recipe.objects.create(
            user=create_user(email='another_user@example.com'),
            title='a recipe',
            directions=['step 1', 'step 2']
        )
        response = self.client.get(RECIPE_URL, **self.headers)
        content = json.loads(response.content.decode('utf-8'))

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        expected = [{'id': recipe_1.id, 'title': recipe_1.title}]

        self.assertEqual(content, expected)

    def test_create_recipe(self):
        """Test creating a recipe."""
        payload = {
            'title': 'a title',
            'directions': ['step 1', 'step 2'],
            'description': 'a description',
            'servings': 1,
            'time_minutes': 10,
            'notes': 'a note',
        }
        response = self.client.post(
            RECIPE_URL,
            data=json.dumps(payload),
            content_type='application/json',
            **self.headers
        )
        content = json.loads(response.content.decode('utf-8'))

        # 201 - CREATED
        self.assertEqual(response.status_code, 201)
        for field, value in payload.items():
            self.assertEqual(content[field], value)

    def test_create_recipe_with_tags(self):
        """
        Test creating a recipe with tags retrieve tags by name correctly or
        create a new one if a tag does not exist.
        """
        existing_tag = Tag.objects.create(name='existing tag')
        new_tag_name = 'new tag'
        payload = {
            'title': 'a title',
            'directions': ['step 1', 'step 2'],
            'description': 'a description',
            'tags': [existing_tag.name, new_tag_name]
        }
        response = self.client.post(
            RECIPE_URL,
            data=json.dumps(payload),
            content_type='application/json',
            **self.headers
        )
        content = json.loads(response.content.decode('utf-8'))

        # 201 - CREATED
        self.assertEqual(response.status_code, 201)
        self.assertEqual(content['tags'], payload['tags'])
        self.assertTrue(Tag.objects.filter(name=new_tag_name).exists())
