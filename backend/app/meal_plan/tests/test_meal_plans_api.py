"""
Tests for the meal-plans API.
"""

import json

from datetime import timedelta
from django.test import Client, TestCase
from django.utils import timezone
from django.urls import reverse

from app.utils_test import create_user, auth_header
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
