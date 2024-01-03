"""
Tests for the recipes API.
"""

import json

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from os import path

from app.utils_test import (
    create_user,
    auth_header,
    create_sample_image,
    create_recipe,
    create_recipe_ing
)
from recipe.models import Recipe, Tag
from ingredient.models import Ingredient, RecipeIngredient, MeasurementUnits


User = get_user_model()
RECIPE_URL = reverse('api:recipes')


def recipe_detail_url(recipe_id):
    """Return a recipe detail URL."""
    return reverse('api:recipe_detail', args=[recipe_id])


def recipe_image_url(recipe_id):
    """Return a recipe_image URL."""
    return reverse('api:recipe_image', args=[recipe_id])


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
        """Test retrieving recipes list only returns own recipes."""
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

    def test_filter_recipes_by_tags(self):
        """Test filtering recipes by tags."""
        tag_1 = Tag.objects.create(name='tag_1')
        tag_2 = Tag.objects.create(name='tag_2')
        recipe_1 = create_recipe(user=self.user, tags=[tag_1.name, tag_2.name])
        recipe_2 = create_recipe(user=self.user, tags=[tag_1.name])
        create_recipe(user=self.user, tags=[tag_2.name])

        params = {'tags': f'{tag_1.name},another_tag'}
        response = self.client.get(RECIPE_URL, params, **self.headers)
        content = json.loads(response.content.decode('utf-8'))

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        expected = [
            {'id': recipe_1.id, 'title': recipe_1.title},
            {'id': recipe_2.id, 'title': recipe_2.title}
        ]

        self.assertEqual(content, expected)

    def test_filter_recipes_ingredients(self):
        """
        Test recipes can be filtered by ingredient's names and that recipes
        are ordered by the number of ingredients in query matched by the
        recipes.
        """
        recipe_1 = create_recipe(user=self.user)
        recipe_2 = create_recipe(user=self.user)
        create_recipe(user=self.user)

        ing_1 = 'ing 1'
        ing_2 = 'ing 2'

        create_recipe_ing(recipe_1, name=ing_1)
        create_recipe_ing(recipe_2, name=ing_1)
        create_recipe_ing(recipe_2, name=ing_2)

        params = {'ingredients': f'{ing_1},{ing_2}'}
        response = self.client.get(RECIPE_URL, params, **self.headers)
        content = json.loads(response.content.decode('utf-8'))

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        # recipe_2 must come before recipe_1 more ingredients in the query.
        expected = [
            {'id': recipe_2.id, 'title': recipe_1.title},
            {'id': recipe_1.id, 'title': recipe_1.title}
        ]

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

    def test_update_recipe(self):
        """Test updating a recipe."""
        recipe = create_recipe(user=self.user)
        new_data = {
            'title': 'a new title',
            'directions': ['new step 1', 'new step 2'],
            'description': 'a new description',
            'servings': 1,
            'time_minutes': 20,
            'notes': 'some new notes',
            'tags': ['new tag 1', 'new tag 2']
        }
        response = self.client.patch(
            recipe_detail_url(recipe.id),
            data=json.dumps(new_data),
            content_type='application/json',
            **self.headers,
        )
        recipe.refresh_from_db()

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        for attr, value in new_data.items():
            if attr == 'tags':
                tags = []
                for tag in recipe.tags.all().order_by('name'):
                    tags.append(tag.name)
                self.assertEqual(value, tags)
            else:
                self.assertEqual(value, getattr(recipe, attr))

    def test_update_recipe_ingredient(self):
        """Test updating recipe's ingredients."""
        recipe = create_recipe(user=self.user)
        updated_ing_name = 'updated ing'
        create_recipe_ing(recipe=recipe, name=updated_ing_name)
        removed_ing_name = 'removed ing'
        create_recipe_ing(recipe=recipe, name=removed_ing_name)
        new_ing = {'name': 'ing 3 new', 'quantity': '20.00',
                   'display_unit': 'ml'}
        new_data = {
            'ingredients': [
                {'name': updated_ing_name, 'quantity': '10.00',
                 'display_unit': 'unit'},
                new_ing
            ]}
        response = self.client.patch(
            recipe_detail_url(recipe.id),
            data=json.dumps(new_data),
            content_type='application/json',
            **self.headers,
        )
        updated_ing = RecipeIngredient.objects.filter(
            recipe=recipe, ingredient__name=updated_ing_name).first()

        # 200 - OK
        self.assertEqual(response.status_code, 200)
        self.assertEqual(RecipeIngredient.objects.filter(
            recipe=recipe).count(), 2)
        # updated ingredient
        self.assertEqual(
            updated_ing.get_display_quantity(),
            Decimal(new_data['ingredients'][0]['quantity'])
        )
        self.assertEqual(updated_ing.display_unit,
                         new_data['ingredients'][0]['display_unit'])
        # removed ingredient
        self.assertFalse(RecipeIngredient.objects.filter(
            recipe=recipe, ingredient__name=removed_ing_name).exists())
        # new ingredient
        self.assertTrue(RecipeIngredient.objects.filter(
            recipe=recipe, ingredient__name=new_ing['name']))

    def test_delete_recipe(self):
        """Test deleting a recipe."""
        recipe = create_recipe(user=self.user)
        recipe_ing_1 = create_recipe_ing(recipe)
        recipe_ing_2 = create_recipe_ing(recipe, name='ing 2')

        response = self.client.delete(
            recipe_detail_url(recipe.id), **self.headers)

        # 204 - NO CONTENT
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())
        self.assertFalse(
            RecipeIngredient.objects.filter(id=recipe_ing_1.id).exists())
        self.assertFalse(
            RecipeIngredient.objects.filter(id=recipe_ing_2.id).exists())

    def test_get_another_user_recipe(self):
        """
        Test getting another user's recipe is not allowed.
        """
        another_user = create_user(email='another_user@example.com')
        recipe = create_recipe(user=another_user)

        response = self.client.get(
            recipe_detail_url(recipe.id), **self.headers)

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)

    def test_update_another_user_recipe(self):
        """
        Test updating another user's recipe is not allowed.
        """
        another_user = create_user(email='another_user@example.com')
        title = 'a title'
        recipe = create_recipe(user=another_user, title=title)

        response = self.client.patch(
            recipe_detail_url(recipe.id),
            data=json.dumps({'title': 'new title'}),
            content_type='application/json',
            **self.headers
        )

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)
        self.assertEqual(recipe.title, title)

    def test_delete_another_user_recipe(self):
        """
        Test deleting another user's recipe is not allowed.
        """
        another_user = create_user(email='another_user@example.com')
        recipe = create_recipe(user=another_user)

        response = self.client.delete(
            recipe_detail_url(recipe.id), **self.headers)

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)
        self.assertTrue(
            Recipe.objects.filter(id=recipe.id).exists())


class RecipeImageTests(TestCase):
    """Tests for recipe image field."""

    def setUp(self):
        self.user = create_user()
        self.recipe = create_recipe(self.user)
        self.headers = auth_header(self.user)
        self.client = Client()

    def tearDown(self):
        self.recipe.image.delete()

    def test_upload_image(self):
        """Test uploading an image is successful."""
        image = create_sample_image()
        response = self.client.post(
            recipe_image_url(self.recipe.id),
            data={'img': image},
            **self.headers
        )
        self.recipe.refresh_from_db()

        # 201 - OK
        self.assertEqual(response.status_code, 200)
        self.assertTrue(path.exists(self.recipe.image.path))

    def test_delete_image(self):
        """Test deleting a recipe image."""
        image = create_sample_image()
        self.recipe.image = SimpleUploadedFile(
            name='test.jpg', content=image.read(), content_type='image/jpeg')
        self.recipe.save()
        response = self.client.delete(
            recipe_image_url(self.recipe.id), **self.headers)

        # 204 - NO CONTENT
        self.assertEqual(response.status_code, 204)
        self.assertFalse(path.exists(self.recipe.image.path))
