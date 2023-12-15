"""
Tests for ingredient app models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from ingredient.models import Ingredient


User = get_user_model()


class IngredientModelTests(TestCase):
    """Tests for the Ingredient model."""

    def test_create_ingredient_same_name(self):
        """
        Test that creating two ingredients with same name raises
        IntegrityError.
        """
        name = 'ingredient name'
        Ingredient.objects.create(name=name)
        with self.assertRaises(IntegrityError):
            Ingredient.objects.create(name=name)

    def test_delete_user_that_added_ingredient(self):
        """
        Tests that deleting the user that created the ingredient sets
        ingredient's added_by field to None instead of deleting the
        ingredient.
        """
        user = User.objects.create_user(
            email='email@example.com', password='password321')
        ingredient = Ingredient.objects.create(
            name='food name', added_by=user)
        user.delete()
        ingredient.refresh_from_db()

        self.assertIsNone(ingredient.added_by)
