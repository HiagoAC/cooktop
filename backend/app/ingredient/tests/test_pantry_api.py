"""
Tests for the pantry API.
"""
import json

from datetime import datetime, timedelta
from django.test import Client, TestCase
from django.urls import reverse

from app.utils_test import create_user, auth_header
from ingredient.models import Ingredient, IngredientInPantry
from ingredient.tests.utils import get_ing_in_pantry

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
        response = self.client.get(pantry_detail_url(ing_pantry.id))

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)


class PrivatePantryAPITests(TestCase):
    """Test authenticated requests for the pantry api."""

    def setUp(self):
        self.user = create_user()
        self.headers = auth_header(self.user)
        self.client = Client()

    def test_retrieve_pantry_ingredients(self):
        """Test retrieving user's pantry ingredients."""
        ing_1 = get_ing_in_pantry(name='a food', user=self.user)
        ing_2 = get_ing_in_pantry(name='another food', user=self.user)
        response = self.client.get(PANTRY_LIST_URL, **self.headers)
        content = json.loads(response.content.decode('utf-8'))

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        expected = [
            {'id': ing_1.id, 'name': ing_1.ingredient.name},
            {'id': ing_2.id, 'name': ing_2.ingredient.name}
        ]
        self.assertEqual(content, expected)

    def test_pantry_ingridients_limited_to_user(self):
        """
        Test retrieving pantry ingredients is limited to the ones of the
        authenticated user.
        """
        another_user = create_user(email='another_user@example.com')
        ing = get_ing_in_pantry(name='a food', user=self.user)
        get_ing_in_pantry(name='another food', user=another_user)
        response = self.client.get(PANTRY_LIST_URL, **self.headers)
        content = json.loads(response.content.decode('utf-8'))

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        expected = [{'id': ing.id, 'name': ing.ingredient.name},]
        self.assertEqual(content, expected)

    def test_get_pantry_detail(self):
        """Test getting pantry ingredient detail."""
        ing = get_ing_in_pantry(
            name='a food',
            quantity=100,
            measurement_unit='ml',
            expiration=datetime.now().date() + timedelta(days=5),
            user=self.user
        )
        response = self.client.get(pantry_detail_url(ing.id), **self.headers)
        content = json.loads(response.content.decode('utf-8'))

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        expected = {
            'id': ing.id,
            'name': ing.ingredient.name,
            'quantity': float(ing.quantity),
            'measurement_unit': ing.measurement_unit,
            'expiration': ing.expiration.isoformat()
        }

        self.assertEqual(content, expected)

    def test_add_ingredient_to_pantry(self):
        """Test adding ingredient to pantry is successful."""
        payload = {
            'name': 'a food',
            'quantity': 100,
            'measurement_unit': 'ml',
        }
        response = self.client.post(
            PANTRY_LIST_URL,
            data=json.dumps(payload),
            content_type='application/json',
            **self.headers,
        )
        content = json.loads(response.content.decode('utf-8'))

        # 201 - CREATED
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', content)
        for key, value in payload.items():
            self.assertEqual(value, content[key])

    def test_add_existing_ingredient_to_pantry(self):
        """
        Test adding existing ingredient to pantry does not alter Ingredient
        instance.
        """
        ing_name = 'a food'
        another_user = create_user(email='another_user@example.com')
        ingredient = Ingredient.objects.create(
            name='a food', added_by=another_user)
        original_ing_id = ingredient.id
        payload = {
            'name': ing_name,
            'quantity': 100,
            'measurement_unit': 'ml',
        }
        response = self.client.post(
            PANTRY_LIST_URL,
            data=json.dumps(payload),
            content_type='application/json',
            **self.headers,
        )
        content = json.loads(response.content.decode('utf-8'))
        ingredient.refresh_from_db()

        # 201 - CREATED
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ingredient.id, original_ing_id)
        self.assertEqual(ing_name, content['name'])

    def test_update_ing_in_pantry(self):
        """Test updating ingredient in pantry."""
        ing_in_pantry = get_ing_in_pantry(
            quantity=100, measurement_unit='ml', user=self.user)
        payload = {
            'quantity': 200,
            'measurement_unit': 'g'
        }
        response = self.client.patch(
            pantry_detail_url(ing_in_pantry.id),
            data=json.dumps(payload),
            content_type='application/json',
            **self.headers,
        )
        ing_in_pantry.refresh_from_db()

        # 200 - OK
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ing_in_pantry.quantity, payload['quantity'])
        self.assertEqual(
            ing_in_pantry.measurement_unit, payload['measurement_unit'])

    def test_update_ing_in_pantry_name(self):
        """
        Test updating name of IngredientInPantry properly changes reference
        to Ingredient.
        """
        original_name = 'a food'
        ing_in_pantry = get_ing_in_pantry(name=original_name, user=self.user)
        ing = Ingredient.objects.get(name=original_name)
        payload = {'name': 'another name'}
        response = self.client.patch(
            pantry_detail_url(ing_in_pantry.id),
            data=json.dumps(payload),
            content_type='application/json',
            **self.headers,
        )
        ing_in_pantry.refresh_from_db()

        # 200 - OK
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ing_in_pantry.ingredient.name, payload['name'])
        self.assertEqual(ing.name, original_name)

    def test_delete_ing_in_pantry(self):
        """Test deleting ingredient in pantry."""
        ing_in_pantry = get_ing_in_pantry(user=self.user)
        response = self.client.delete(
            pantry_detail_url(ing_in_pantry.id), **self.headers)

        # 204 - NO CONTENT
        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            IngredientInPantry.objects.filter(id=ing_in_pantry.id).exists())

    def test_get_another_user_ing_in_pantry(self):
        """
        Test getting another user's pantry ingredient is not allowed.
        """
        another_user = create_user(email='another_user@example.com')
        ing_in_pantry = get_ing_in_pantry(user=another_user)

        response = self.client.get(
            pantry_detail_url(ing_in_pantry.id), **self.headers)

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)

    def test_update_another_user_ing_in_pantry(self):
        """
        Test updating another user's pantry ingredient is not allowed.
        """
        another_user = create_user(email='another_user@example.com')
        original_quantity = 100
        ing_in_pantry = get_ing_in_pantry(
            quantity=original_quantity, user=another_user)

        response = self.client.patch(
            pantry_detail_url(ing_in_pantry.id),
            data=json.dumps({'quantity': original_quantity + 1}),
            content_type='application/json',
            **self.headers
        )

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)
        self.assertEqual(ing_in_pantry.quantity, original_quantity)

    def test_delete_another_user_ing_in_pantry(self):
        """
        Test deleting another user's pantry ingredient is not allowed.
        """
        another_user = create_user(email='another_user@example.com')
        ing_in_pantry = get_ing_in_pantry(user=another_user)

        response = self.client.delete(
            pantry_detail_url(ing_in_pantry.id), **self.headers)

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)
        self.assertTrue(
            IngredientInPantry.objects.filter(id=ing_in_pantry.id).exists())
