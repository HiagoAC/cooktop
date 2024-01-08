"""Tests for models in the meal_plan app."""

from django.test import TestCase

from app.utils_test import create_meal, create_recipe, create_user
from recipe.models import Recipe
from meal_plan.models import Preferences, Meal, MealPlan


class PreferencesModelTests(TestCase):
    """Tests for the Preferences model."""

    def test_create_preferences(self):
        """Test creating a preferences object."""
        params = {
            'user': create_user(),
            'servings_per_meal': 2,
            'cookings_per_week': 7,
        }
        prefs = Preferences.objects.create(**params)

        for attr, value in params.items():
            self.assertEqual(getattr(prefs, attr), value)


class MealModelTests(TestCase):
    """Tests for the Meal model."""

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


class MealPlanModelTests(TestCase):
    """Tests for the MealPlan model."""

    def test_create_meal_plan(self):
        """Test creating a meal_plan."""
        user = create_user()
        servings_per_meal = 2
        meal_plan = MealPlan.objects.create(
            user=user, servings_per_meal=servings_per_meal)
        meals = dict()
        for day in range(1, 3):
            meals[day] = create_meal(user=user, day=day)
            meal_plan.meals.add(meals[day])
        meal_plan.save()

        self.assertEqual(servings_per_meal, meal_plan.servings_per_meal)
        for _, meal in meals.items():
            self.assertIn(meal, meal_plan.meals.all())
