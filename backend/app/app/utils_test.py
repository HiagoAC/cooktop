"""
Utitility functions for tests.
"""

import jwt

from datetime import timedelta
from django.contrib.auth import get_user_model
from io import BytesIO
from PIL import Image
from time import time
from typing import Dict, List

from ingredient.models import Ingredient, IngredientInPantry, RecipeIngredient
from meal_plan.models import Meal, MealPlan
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


def create_ing_in_pantry(name='food name', quantity=100, measurement_unit='ml',
                         expiration=None, user=None, ingredient=None):
    """Returns an instance of IngredientInPantry."""
    if not user:
        user = create_user()
    if not ingredient:
        ingredient = Ingredient.objects.create(name=name)
    ing_in_pantry = IngredientInPantry.objects.create(
        user=user,
        ingredient=ingredient,
        quantity=quantity,
        measurement_unit=measurement_unit,
        expiration=expiration
    )
    return ing_in_pantry


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


def create_recipes_dict(
        user, main_dish=0, side_dish=0, salad=0, snack=0, dessert=0
        ) -> Dict[str, List[Recipe]]:
    """Create a dictionary of recipes by type."""
    recipes = dict()
    recipes['main_dish'] = [
        create_recipe(user=user, recipe_type=Recipe.RecipeTypes.MAIN_DISH)
        for _ in range(main_dish)
        ]
    recipes['side_dish'] = [
        create_recipe(user=user, recipe_type=Recipe.RecipeTypes.SIDE_DISH)
        for _ in range(side_dish)
        ]
    recipes['salad'] = [
        create_recipe(user=user, recipe_type=Recipe.RecipeTypes.SALAD)
        for _ in range(salad)
        ]
    recipes['snack'] = [
        create_recipe(user=user, recipe_type=Recipe.RecipeTypes.SNACK)
        for _ in range(snack)
        ]
    recipes['dessert'] = [
        create_recipe(user=user, recipe_type=Recipe.RecipeTypes.DESSERT)
        for _ in range(dessert)
        ]

    return recipes


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


def create_sample_meal_plan(user, cookings=3):
    """
    Create and return a sample meal plan with meals.
    This sample does not generate a meal plan with MealPlanner.
    """
    meal_plan = MealPlan.objects.create(user=user)
    for day in range(1, cookings):
        meal_plan.meals.add(create_meal(user=user, day=day))
    return meal_plan
