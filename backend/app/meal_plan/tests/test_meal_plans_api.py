"""
Tests for the meal-plans API.
"""

import json

from datetime import timedelta
from django.test import Client, TestCase
from django.utils import timezone
from django.urls import reverse
from unittest.mock import patch

from app.utils_test import create_user, auth_header
from ingredient.models import Ingredient
from meal_plan.models import MealPlan


PLAN_URL = reverse('api:meal_plans')


def plan_detail_url(meal_plan_id):
    """Return a meal_plan detail URL."""
    return reverse('api:meal_plan_detail', args=[meal_plan_id])


class PublicMealPlansAPITests(TestCase):
    """Test unauthenticated requests to the meal_plans API."""

    def setUp(self):
        self.client = Client()

    def test_unauthenticated_recipe_list_request(self):
        """
        Test that retrieving recipes list unauthenticated is
        unauthorized.
        """
        response = self.client.get(PLAN_URL)

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)


class PrivateMealPlansAPITests(TestCase):
    """Test authenticated requests for the meal_plans API."""

    def setUp(self):
        self.user = create_user()
        self.headers = auth_header(self.user)
        self.client = Client()

    def test_retrieve_meal_plan_list(self):
        """Test retrieving meal plan list authenticated."""
        plan_1 = MealPlan.objects.create(user=self.user)
        plan_1.creation_date = timezone.now() - timedelta(days=8)
        plan_1.save()
        plan_2 = MealPlan.objects.create(user=self.user)

        response = self.client.get(PLAN_URL, **self.headers)
        content = json.loads(response.content.decode('utf-8'))

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        expected = list()
        for plan in (plan_2, plan_1):
            expected.append({
                'id': plan.id,
                'creation_date': plan.creation_date.strftime('%Y-%m-%d')
            })

        self.assertEqual(content, expected)

    def test_retrieve_meal_plan_list_another_user(self):
        """
        Test retrieving meal plan list does not return meal plans of other
        users.
        """
        plan = MealPlan.objects.create(user=self.user)
        MealPlan.objects.create(
            user=create_user(email='another_user@example.com'))

        response = self.client.get(PLAN_URL, **self.headers)
        content = json.loads(response.content.decode('utf-8'))

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        expected = [{
                'id': plan.id,
                'creation_date': plan.creation_date.strftime('%Y-%m-%d')
            }]

        self.assertEqual(content, expected)

    @patch('meal_plan.api.MealPlanner.generate_plan')
    def test_create_meal_plan(self, mock_generate_plan):
        """Test creating a meal plan."""
        meal_plan = MealPlan.objects.create(user=self.user)
        mock_generate_plan.return_value = meal_plan
        ing_1, ing_2 = 'ing_1', 'ing_2'
        Ingredient.objects.create(name=ing_1)
        Ingredient.objects.create(name=ing_2)
        payload = {
            'requested_ingredients': ['ing_1', 'ing_2'],
            'cookings': 4,
            'servings_per_meal': 5
        }
        response = self.client.post(
            PLAN_URL,
            data=json.dumps(payload),
            content_type='application/json',
            **self.headers
        )
        content = json.loads(response.content.decode('utf-8'))
        # 201 - CREATED
        self.assertEqual(response.status_code, 201)
        mock_generate_plan.assert_called_once_with(**payload)
        self.assertIn('meals', content)
