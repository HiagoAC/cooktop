"""
Tests for the meal_planner module.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from app.utils_test import create_recipes_dict, create_user
from meal_plan.meal_planner import MealPlanner

User = get_user_model()


class MealPlannerTests(TestCase):
    """Tests for the MealPlanner class."""
    def setUp(self):
        self.user = create_user()
        self.meal_planner = MealPlanner(user=self.user)

    def test_create_meal_planner(self):
        """Test creating a meal planner object."""
        recipes = create_recipes_dict(
            user=self.user, main_dish=2, side_dish=1,
            salad=1, snack=1, dessert=1)
        meal_planner = MealPlanner(user=self.user)

        for attr, values in recipes.items():
            if attr in ('main_dish', 'side_dish', 'salad'):
                self.assertEqual(
                    len(values), meal_planner.user_recipes[attr].count())
                for value in values:
                    self.assertIn(value, meal_planner.user_recipes[attr])
