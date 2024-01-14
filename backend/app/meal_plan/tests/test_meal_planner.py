"""
Tests for the meal_planner module.
"""

from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch

from app.utils_test import (
    create_ing_in_pantry,
    create_recipe,
    create_recipe_ing,
    create_recipes_dict,
    create_user
)
from meal_plan.meal_planner import MealPlanner
from recipe.models import Recipe

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
        """Test private method _filter_user_recipes_by_ingredients."""
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

    def test_reorder_by_expiring_ings(self):
        """
        Test that recipes with expiring ingredients appear before recipes
        without expiring ingredients in the returned querysets of private
        method _reorder_by_expiring_ings.
        """
        expiring_ing = 'expiring'
        not_expiring_ing = 'not expiring'
        create_ing_in_pantry(
            user=self.user,
            name=expiring_ing,
            expiration=timezone.now().date() + timedelta(days=6)
        )
        create_ing_in_pantry(
            user=self.user,
            name=not_expiring_ing,
            expiration=timezone.now().date() + timedelta(days=8)
        )
        with_expiring = 'B - expiring'
        not_expiring = 'A - not expiring'
        recipe_dict = dict()
        for recipe_type in (
            Recipe.RecipeTypes.MAIN_DISH,
            Recipe.RecipeTypes.SIDE_DISH,
            Recipe.RecipeTypes.SALAD
        ):
            recipe_exp = create_recipe(
                user=self.user, title=with_expiring, recipe_type=recipe_type)
            create_recipe_ing(
                recipe=recipe_exp,
                name=expiring_ing
            )
            recipe_not_exp = create_recipe(
                user=self.user, title=not_expiring, recipe_type=recipe_type)
            create_recipe_ing(
                recipe=recipe_not_exp,
                name=not_expiring_ing
            )
            # make recipes with no expiring ings first in querysets
            recipe_dict[recipe_type] = Recipe.objects.filter(
                recipe_type=recipe_type).order_by('title')

        recipes = self.meal_planner._reorder_by_expiring_ings(
            recipe_dict)

        for _, queryset in recipes.items():
            recipe_exp = queryset.filter(title=with_expiring).first()
            recipe_not_exp = queryset.filter(title=not_expiring).first()
            qs_list = list(queryset)

            self.assertTrue(
                qs_list.index(recipe_exp) < qs_list.index(recipe_not_exp))

    @patch('meal_plan.meal_planner.choice')
    def test_pick_random_recipe(self, mock_choice):
        """Test picking a random recipe with _pick_random_recipe."""
        recipe = self.recipes['main_dish'][0]
        mock_choice.return_value = recipe.id
        picked_recipe = self.meal_planner._pick_random_recipe(
            self.meal_planner.user_recipes['main_dish'])

        self.assertEqual(recipe, picked_recipe)

    def test_pick_recipe_by_index(self):
        """
        Test picking a recipe in a queryset by indeces in and out of range
        with _pick_recipe_by_index.
        """
        queryset = self.meal_planner.user_recipes['side_dish']
        for i in range(len(queryset)):
            recipe_1 = self.meal_planner._pick_recipe_by_index(queryset, i)
            recipe_2 = self.meal_planner._pick_recipe_by_index(
                queryset, i + len(queryset))

            self.assertEqual(recipe_1, queryset[i])
            self.assertEqual(recipe_1, recipe_2)

    def test_make_meals(self):
        """
        - Test making meals with a main dish, a side dish and a salad with
        _make_meals.
        - It tests the case where there are enough recipes of each type in the
        queryset.
        """
        querysets = self.meal_planner.user_recipes
        number_meals = min(qs.count() for qs in querysets.values())
        meals = self.meal_planner._make_meals(querysets, number_meals)

        for i in range(number_meals):
            self.assertEqual(meals[i].main_dish, querysets['main_dish'][i])
            self.assertEqual(meals[i].side_dish, querysets['side_dish'][i])
            self.assertEqual(meals[i].salad, querysets['salad'][i])
