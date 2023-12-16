"""
Tests for the apis in the ingredient app.
"""
import json
import jwt

from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from time import time

from ingredient.tests.utils import get_ing_in_pantry
from user.auth_handler import JWT_SECRET, JWT_ALGO


User = get_user_model()
PANTRY_LIST_URL = reverse('api:pantry_list')


def pantry_detail_url(ing_pantry_id):
    """
    Returns a pantry detail URL.
    """
    return reverse('api:pantry_detail', args=[ing_pantry_id])


class PublicPantryAPITests(TestCase):
    """Test unauthenticated requests to the pantry API."""

    def setUp(self):
        self.client = Client()

    def test_unauthenticated_list_request(self):
        """
        Test that retrieving pantry ingredients list unauthenticated is
        unauthorized.
        """
        response = self.client.get(PANTRY_LIST_URL)

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_detail_request(self):
        """
        Test that retrieving pantry ingredient detail unauthenticated is
        unauthorized.
        """
        ing_pantry = get_ing_in_pantry()
        response = self.client.get(pantry_detail_url(ing_pantry.pk))

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)


class PrivatePantryAPITests(TestCase):
    """Test authenticated requests for the pantry api."""

    def setUp(self):
        email = 'email@example.com'
        self.user = User.objects.create(
            email=email, password='password321')
        token_data = {
            'email': email,
            'exp': time() + timedelta(minutes=10).total_seconds(),
            'sub': 'access_token',
        }
        access_token = jwt.encode(token_data, JWT_SECRET, algorithm=JWT_ALGO)
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        self.client = Client()

    def test_retrieve_pantry_ingredients(self):
        """Test retrieving user's pantry's ingredients."""
        ing_1 = get_ing_in_pantry(name='a food', user=self.user)
        ing_2 = get_ing_in_pantry(name='another food', user=self.user)
        response = self.client.get(PANTRY_LIST_URL, **self.headers)

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        # Parse content
        content = json.loads(response.content.decode('utf-8'))

        expected = [
            {'id': ing_1.pk, 'name': ing_1.ingredient.name},
            {'id': ing_2.pk, 'name': ing_2.ingredient.name}
        ]
        self.assertEqual(content, expected)
