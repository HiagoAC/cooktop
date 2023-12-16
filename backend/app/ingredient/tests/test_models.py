"""
Tests for ingredient app models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from ingredient.models import Ingredient, IngredientInPantry


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


class IngredientInPantryModelTests(TestCase):
    """Tests for IngredientInPantry model."""

    def get_ing_in_pantry(self, quantity=100, measurement_unit='ml'):
        """Returns an instance of IngredientInPantry."""
        user = User.objects.create_user(
            email='email@example.com', password='password321')
        ingredient = Ingredient.objects.create(name='food name')
        ing_in_pantry = IngredientInPantry.objects.create(
            user=user,
            ingredient=ingredient,
            quantity=quantity,
            measurement_unit=measurement_unit
        )
        return ing_in_pantry

    def test_create_ing_in_pantry_same_user_and_ingredient(self):
        """
        Test that creating two IngredientInPantry objects with same user and
        ingredient raises IntegrityError.
        """
        self.get_ing_in_pantry()
        with self.assertRaises(IntegrityError):
            self.get_ing_in_pantry(200, 'g')

    def test_subtract_quantity(self):
        """
        Test that subtract_quantity succeeds in subtracting from quantity.
        """
        original_quantity = 100
        ing_in_pantry = self.get_ing_in_pantry(original_quantity)
        sub_quantity = 50
        ing_in_pantry.subtract_quantity(
            sub_quantity, ing_in_pantry.measurement_unit)

        self.assertEqual(
            ing_in_pantry.quantity, original_quantity - sub_quantity)

    def test_subtract_more_than_quantity(self):
        """
        Test that calling subtract_quantity with a value superior to object's
        quantity sets quantity to 0.
        """
        ing_in_pantry = self.get_ing_in_pantry()
        sub_quantity = ing_in_pantry.quantity + 1
        ing_in_pantry.subtract_quantity(
            sub_quantity, ing_in_pantry.measurement_unit)

        self.assertEqual(ing_in_pantry.quantity, 0)

    def test_subtract_with_wrong_unit(self):
        """
        Test that calling subtract_quantity with a mismatched unit raises a
        ValueError.
        """
        ing_in_pantry = self.get_ing_in_pantry(measurement_unit='g')
        with self.assertRaises(ValueError):
            ing_in_pantry.subtract_quantity(50, 'ml')
