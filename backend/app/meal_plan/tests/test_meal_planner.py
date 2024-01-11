"""
Tests for the meal_planner module.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from app.utils_test import (
    create_ing_in_pantry,
    create_recipe_ing,
    create_recipes_dict,
    create_user
)
from meal_plan.meal_planner import MealPlanner

User = get_user_model()


class MealPlannerTests(TestCase):
    """Tests for the MealPlanner class."""
    def setUp(self):
        self.user = create_user()
        self.recipes = create_recipes_dict(
            user=self.user, main_dish=4, side_dish=3, salad=2)
        self.meal_planner = MealPlanner(user=self.user)

    def test_create_meal_planner(self):
        """Test creating a meal planner object."""
        for attr, values in self.recipes.items():
            if attr in ('main_dish', 'side_dish', 'salad'):
                self.assertEqual(
                    len(values), self.meal_planner.user_recipes[attr].count())
                for value in values:
                    self.assertIn(value, self.meal_planner.user_recipes[attr])

    def test_filter_user_recipes_by_ingredients(self):
        """Test _filter_user_recipes_by_ingredients."""
        # create ingredients in recipes
        requested_ingredients = [f'ing_{i}' for i in range(3)]
        for t, ing in zip(('main_dish', 'side_dish', 'salad'),
                          requested_ingredients):
            create_recipe_ing(self.recipes[t][1], name=ing)
        # add ingredient not in recipes to requested ingredients
        requested_ingredients.append(f'ing_{len(requested_ingredients) - 1}')
        # add ingredients to pantry
        for i in range(2):
            ing_name = f'ing_pantry_{i + len(requested_ingredients) - 1}'
            create_ing_in_pantry(
                user=self.user,
                name=ing_name
                )
            create_recipe_ing(self.recipes['main_dish'][i], name=ing_name)
        # add not requested ingredients to recipes
        create_recipe_ing(self.recipes['main_dish'][3], name='not_requested')
        create_recipe_ing(self.recipes['side_dish'][2], name='also_not')

        filtered_recipes = self.meal_planner\
            ._filter_user_recipes_by_ingredients(requested_ingredients)

        self.assertEqual(filtered_recipes['main_dish'].count(), 2)
        self.assertEqual(
            self.recipes['main_dish'][1], filtered_recipes['main_dish'][0])
        self.assertEqual(
            self.recipes['main_dish'][0], filtered_recipes['main_dish'][1])
        self.assertEqual(filtered_recipes['side_dish'].count(), 1)
        self.assertEqual(
            self.recipes['side_dish'][1], filtered_recipes['side_dish'][0])
        self.assertEqual(filtered_recipes['salad'].count(), 1)
        self.assertEqual(
            self.recipes['salad'][1], filtered_recipes['salad'][0])
