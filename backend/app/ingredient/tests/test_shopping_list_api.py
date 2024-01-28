"""
Tests for the shopping list API.
"""
import json

from django.test import Client, TestCase
from django.urls import reverse

from app.utils_test import auth_header, create_shopping_list_item, create_user
from ingredient.schemas import ShoppingListItemOut

SHOPPING_LIST_URL = reverse('api:shopping_list')


def shopping_item_detail_url(item_id):
    """
    Returns a shopping list item detail URL.
    """
    return reverse('api:shopping_item_detail', args=[item_id])


class PublicPantryAPITests(TestCase):
    """Test unauthenticated requests to the pantry API."""

    def setUp(self):
        self.client = Client()

    def test_unauthenticated_list_request(self):
        """
        Test that retrieving shopping item list unauthenticated is
        unauthorized.
        """
        response = self.client.get(SHOPPING_LIST_URL)

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_detail_request(self):
        """
        Test that retrieving shopping item detail unauthenticated is
        unauthorized.
        """
        item = create_shopping_list_item(user=create_user())
        response = self.client.get(shopping_item_detail_url(item.id))

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)


class PrivatePantryAPITests(TestCase):
    """Test authenticated requests for the pantry api."""

    def setUp(self):
        self.user = create_user()
        self.headers = auth_header(self.user)
        self.client = Client()

    def test_retrieve_shopping_list(self):
        """Test retrieving user's shopping list."""
        item_1 = create_shopping_list_item(user=self.user, name='a food')
        item_2 = create_shopping_list_item(user=self.user, name='another food')
        response = self.client.get(SHOPPING_LIST_URL, **self.headers)
        content = json.loads(response.content.decode('utf-8'))

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        expected = [
            ShoppingListItemOut.from_orm(item_1).dict(),
            ShoppingListItemOut.from_orm(item_2).dict()
            ]
        self.assertEqual(content, expected)

    def test_retrieve_shopping_list_limited_to_user(self):
        """
        Test retrieving shopping list is limited to the ones of the
        authenticated user.
        """
        another_user = create_user(email='another_user@example.com')
        item = create_shopping_list_item(user=self.user, name='a food')
        create_shopping_list_item(user=another_user, name='another food')
        response = self.client.get(SHOPPING_LIST_URL, **self.headers)
        content = json.loads(response.content.decode('utf-8'))

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        expected = [ShoppingListItemOut.from_orm(item).dict()]
        self.assertEqual(content, expected)

    def test_get_shopping_item_detail(self):
        """Test getting shopping item detail."""
        item = create_shopping_list_item(
            user=self.user,
            name='a food',
            quantity=100,
            display_unit='cup',
        )
        response = self.client.get(
            shopping_item_detail_url(item.id), **self.headers)
        content = json.loads(response.content.decode('utf-8'))

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        expected = ShoppingListItemOut.from_orm(item).dict()

        self.assertEqual(content, expected)
