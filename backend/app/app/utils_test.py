"""
Utitility functions for tests.
"""

import jwt

from datetime import timedelta
from django.contrib.auth import get_user_model
from io import BytesIO
from PIL import Image
from time import time

from ingredient.models import Ingredient, RecipeIngredient
from meal_plan.models import Meal
from recipe.models import Recipe, Tag
from user.auth_handler import JWT_SECRET, JWT_ALGO


def create_user(email='example@test.com'):
    """Create a user."""
    return get_user_model().objects.create_user(
        email=email, password='password321')


def auth_header(user):
    """Return a header with a valid token for the given user."""
    token_data = {
        'email': user.email,
        'exp': time() + timedelta(minutes=10).total_seconds(),
        'sub': 'access_token',
    }
    access_token = jwt.encode(token_data, JWT_SECRET, algorithm=JWT_ALGO)
    headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
    return headers


def create_sample_image():
    """Return an in-memory file-like image object."""
    image = Image.new('RGB', (100, 100))
    image_io = BytesIO()
    image.save(image_io, format='JPEG')
    image_io.seek(0)

    return image_io


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
        'recipe_type': Recipe.RecipeTypes.MAIN_DISH,
        'notes': 'some notes'
    }
    recipe_data.update(params)
    recipe = Recipe.objects.create(user=user, **recipe_data)

    for tag_name in tags:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        if created:
            tag.added_by = user
        recipe.tags.add(tag)

    recipe.save()
    return recipe


def create_meal(user, **params):
    """Create and return a meal."""
    meal_data = {
        'main_dish': create_recipe(
                user=user, recipe_type=Recipe.RecipeTypes.MAIN_DISH),
        'side_dish': create_recipe(
                user=user, recipe_type=Recipe.RecipeTypes.SIDE_DISH),
        'salad': create_recipe(
                user=user, recipe_type=Recipe.RecipeTypes.SALAD),
        'day': 1
    }
    meal_data.update(params)
    meal = Meal.objects.create(**meal_data)
    return meal
