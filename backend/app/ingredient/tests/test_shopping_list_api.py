"""
Tests for the shopping list API.
"""
from decimal import Decimal
import json

from django.test import Client, TestCase
from django.urls import reverse

from app.utils_test import (
    auth_header,
    create_ing_in_pantry,
    create_shopping_list_item,
    create_user
)
from ingredient.models import Ingredient, IngredientInPantry, ShoppingListItem
from ingredient.schemas import ShoppingListItemOut

SHOPPING_LIST_URL = reverse('api:shopping_list')
ADD_LIST_TO_PANTRY_URL = reverse('api:add_list_to_pantry')
CLEAR_LIST_URL = reverse('api:clear_shopping_list')


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

    def test_add_items_to_pantry(self):
        """Test adding shopping list items to pantry."""
        original_quantity = 100
        pantry_item = create_ing_in_pantry(
            user=self.user,
            name='food 0',
            quantity=original_quantity,
            display_unit='cup'
        )
        items = []
        add_quantity = 50
        for i in range(2):
            items.append(create_shopping_list_item(
                    user=self.user,
                    name=f'food {i}',
                    display_unit='cup',
                    quantity=add_quantity
                ))
        response = self.client.post(ADD_LIST_TO_PANTRY_URL, **self.headers)

        pantry_item.refresh_from_db()
        # 200 - OK
        self.assertEqual(response.status_code, 200)
        self.assertEqual(pantry_item.get_display_quantity(),
                         original_quantity + add_quantity)
        self.assertEqual(IngredientInPantry.objects.get(
            user=self.user, ingredient__name='food 1')
            .get_display_quantity(), add_quantity)

    def test_clear_list(self):
        """Test clearing shopping list."""
        items = []
        for i in range(2):
            items.append(create_shopping_list_item(
                user=self.user, name=f'food {i}'))
        response = self.client.delete(CLEAR_LIST_URL, **self.headers)

        # 204 - NO CONTENT
        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            ShoppingListItem.objects.filter(user=self.user).exists())

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
            quantity='100.00',
            display_unit='cup',
        )
        response = self.client.get(
            shopping_item_detail_url(item.id), **self.headers)
        content = json.loads(response.content.decode('utf-8'))

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        expected = ShoppingListItemOut.from_orm(item).dict()

        self.assertEqual(content, expected)

    def test_add_item_to_shopping_list(self):
        """Test adding item to shopping list is successful."""
        payload = {
            'name': 'a food',
            'quantity': '2.00',
            'unit': 'cup',
        }
        response = self.client.post(
            SHOPPING_LIST_URL,
            data=json.dumps(payload),
            content_type='application/json',
            **self.headers,
        )
        content = json.loads(response.content.decode('utf-8'))

        # 201 - CREATED
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', content)
        payload['quantity'] = Decimal(payload['quantity'])
        for key, value in payload.items():
            self.assertEqual(value, content[key])

    def test_add_to_shopping_list_with_existing_item(self):
        """
        Test adding to the shopping list with an item that already exists
        correctly adds to quantity and does not create a new item.
        """
        name = 'a food'
        item = create_shopping_list_item(user=self.user, name=name)
        payload = {
            'name': name,
            'quantity': '2.00',
            'unit': 'cup',
        }
        final_quantity = item.get_display_quantity() + \
            Decimal(payload['quantity'])
        response = self.client.post(
            SHOPPING_LIST_URL,
            data=json.dumps(payload),
            content_type='application/json',
            **self.headers,
        )
        content = json.loads(response.content.decode('utf-8'))

        # 201 - CREATED
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', content)
        self.assertEqual(ShoppingListItem.objects.filter(
            ingredient__name=name, user=self.user).count(), 1)
        self.assertEqual(final_quantity, content['quantity'])

    def test_update_shopping_item(self):
        """Test updating shopping list item."""
        item = create_shopping_list_item(
            user=self.user,
            name='a food',
            quantity='3.00',
            display_unit='cup',
        )
        payload = {
            'quantity': '200.00',
            'unit': 'gram'
        }
        response = self.client.patch(
            shopping_item_detail_url(item.id),
            data=json.dumps(payload),
            content_type='application/json',
            **self.headers,
        )
        item.refresh_from_db()

        # 200 - OK
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            item.get_display_quantity(), Decimal(payload['quantity']))
        self.assertEqual(item.display_unit, payload['unit'])

    def test_update_shopping_item_name(self):
        """
        Test updating name of a shopping list item properly changes reference
        to Ingredient.
        """
        original_name = 'a food'
        item = create_shopping_list_item(
            user=self.user, name=original_name)
        ing = Ingredient.objects.get(name=original_name)
        payload = {'name': 'new name'}
        response = self.client.patch(
            shopping_item_detail_url(item.id),
            data=json.dumps(payload),
            content_type='application/json',
            **self.headers,
        )
        item.refresh_from_db()

        # 200 - OK
        self.assertEqual(response.status_code, 200)
        self.assertEqual(item.ingredient.name, payload['name'])
        self.assertEqual(ing.name, original_name)

    def test_delete_shopping_list_item(self):
        """Test deleting shopping list item."""
        item = create_shopping_list_item(user=self.user)
        response = self.client.delete(
            shopping_item_detail_url(item.id), **self.headers)

        # 204 - NO CONTENT
        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            ShoppingListItem.objects.filter(id=item.id).exists())

    def test_get_another_user_shopping_list_item(self):
        """
        Test getting another user's shopping list item is not allowed.
        """
        another_user = create_user(email='another_user@example.com')
        item = create_shopping_list_item(user=another_user)

        response = self.client.get(
            shopping_item_detail_url(item.id), **self.headers)

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)

    def test_update_another_user_shopping_list_item(self):
        """
        Test updating another user's shopping list item is not allowed.
        """
        another_user = create_user(email='another_user@example.com')
        original_quantity = '3.00'
        item = create_shopping_list_item(
            user=another_user, quantity=original_quantity)

        response = self.client.patch(
            shopping_item_detail_url(item.id),
            data=json.dumps({'quantity': '4.00'}),
            content_type='application/json',
            **self.headers
        )
        item.refresh_from_db()
        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            item.get_display_quantity(), Decimal(original_quantity))

    def test_delete_another_user_shopping_list_item(self):
        """
        Test deleting another user's shopping list item is not allowed.
        """
        another_user = create_user(email='another_user@example.com')
        item = create_shopping_list_item(user=another_user)

        response = self.client.delete(
            shopping_item_detail_url(item.id), **self.headers)

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)
        self.assertTrue(
            ShoppingListItem.objects.filter(id=item.id).exists())
