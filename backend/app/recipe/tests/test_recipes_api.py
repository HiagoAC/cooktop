"""
Tests for the recipes API.
"""

import json

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from app.utils_test import create_user, auth_header
from recipe.models import Recipe, Tag
from ingredient.models import Ingredient, RecipeIngredient, MeasurementUnits


User = get_user_model()
RECIPE_URL = reverse('api:recipes')


def recipe_detail_url(recipe_id):
    """Return a recipe detail URL."""
    return reverse('api:recipe_detail', args=[recipe_id])


def create_recipe_ing(recipe, name='ing 1', **params):
    """Create and return a RecipeIngredient instance."""
    ingredient, _ = Ingredient.objects.get_or_create(name=name)
    data = {
        'quantity': '2.00',
        'display_unit': 'cup'
    }
    data.update(params)
    recipe_ing = RecipeIngredient.create_with_display_unit(
        recipe=recipe, ingredient=ingredient, **data)
    return recipe_ing


def create_recipe(user, tags=['tag 1', 'tag 2'], **params):
    """Create and return a recipe with tags."""
    recipe_data = {
        'title': 'a title',
        'directions': ['step 1', 'step 2'],
        'description': 'a description',
        'servings': 2,
        'time_minutes': 10,
        'notes': 'some notes'
    }
    recipe_data.update(params)
    recipe = Recipe.objects.create(user=user, **recipe_data)

    for tag_name in tags:
        tag = Tag.objects.create(name=tag_name, added_by=user)
        recipe.tags.add(tag)

    recipe.save()
    return recipe


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

    def test_create_recipe_with_ingredients(self):
        """
        Test creating a recipe with ingredients properly create
        RecipeIngredient instances, and Ingredient if it does not exist.
        """
        existing_ing = Ingredient.objects.create(name='existing ingredient')
        new_ing_name = 'new ingredient'
        recipe_ings = [
            {'name': existing_ing.name, 'quantity': '2.00',
             'display_unit': 'cup'},
            {'name': new_ing_name, 'quantity': '100.00',
             'display_unit': 'ml'}
        ]
        payload = {
            'title': 'a title',
            'directions': ['step 1', 'step 2'],
            'description': 'a description',
            'ingredients': recipe_ings,
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
        self.assertEqual(content['ingredients'], payload['ingredients'])

        recipe = Recipe.objects.get(id=content['id'])
        new_ing = Ingredient.objects.get(name=new_ing_name)
        recipe_existing_ing = RecipeIngredient.objects.filter(
            recipe=recipe, ingredient=existing_ing).first()

        self.assertTrue(RecipeIngredient.objects.filter(
            recipe=recipe, ingredient=new_ing).exists())
        # 2 cups = 473.18 ml
        self.assertEqual(recipe_existing_ing.quantity, Decimal('473.18'))
        self.assertEqual(recipe_existing_ing.measurement_unit,
                         MeasurementUnits.MILLILITER)

    def test_get_recipe_detail(self):
        """Test getting recipe detail."""
        tags = ['tag 1', 'tag 2']
        recipe = create_recipe(user=self.user, tags=tags)
        quantity = '2.00'
        ing_1 = create_recipe_ing(recipe=recipe, quantity=quantity)
        ing_2 = create_recipe_ing(recipe=recipe, name='another ingredient',
                                  quantity=quantity)
        recipe_ings = [
            {'name': ing_1.ingredient.name, 'quantity': quantity,
             'display_unit': ing_1.display_unit},
            {'name': ing_2.ingredient.name, 'quantity': quantity,
             'display_unit': ing_2.display_unit}
        ]

        response = self.client.get(
            recipe_detail_url(recipe.id), **self.headers)
        content = json.loads(response.content.decode('utf-8'))

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        for attr, value in content.items():
            if attr == 'tags':
                self.assertEqual(value, tags)
            elif attr == 'ingredients':
                self.assertEqual(value, recipe_ings)
            else:
                self.assertEqual(value, getattr(recipe, attr))
