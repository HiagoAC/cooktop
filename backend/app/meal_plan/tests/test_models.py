"""Tests for models in the meal_plan app."""

from django.test import TestCase

from app.utils_test import create_recipe, create_user
from recipe.models import Recipe
from meal_plan.models import Preferences, Meal


class PreferencesModelTests(TestCase):
    """Tests for the Preferences model."""

    def test_create_preferences(self):
        """Test creating a preferences object."""
        params = {
            'user': create_user(),
            'servings_per_week': 14,
            'cookings_per_week': 7,
        }
        prefs = Preferences.objects.create(**params)

        for attr, value in params.items():
            self.assertEqual(getattr(prefs, attr), value)

    def test_create_meal(self):
        """Test creating a meal."""
        user = create_user()
        params = {
            'main_dish': create_recipe(
                user=user, recipe_type=Recipe.RecipeTypes.MAIN_DISH),
            'side_dish': create_recipe(
                user=user, recipe_type=Recipe.RecipeTypes.SIDE_DISH),
            'salad': create_recipe(
                user=user, recipe_type=Recipe.RecipeTypes.SALAD),
            'day': 1
        }
        meal = Meal.objects.create(**params)

        for attr, value in params.items():
            self.assertEqual(getattr(meal, attr), value)
