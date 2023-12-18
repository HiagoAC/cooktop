"""
Tests for ingredient app models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from app.utils_test import create_user
from ingredient.models import Ingredient, RecipeIngredient
from ingredient.tests.utils import get_ing_in_pantry
from recipe.models import Recipe

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
        user = create_user()
        ingredient = Ingredient.objects.create(
            name='food name', added_by=user)
        user.delete()
        ingredient.refresh_from_db()

        self.assertIsNone(ingredient.added_by)


class IngredientInPantryModelTests(TestCase):
    """Tests for IngredientInPantry model."""

    def test_create_ing_in_pantry_same_user_and_ingredient(self):
        """
        Test that creating two IngredientInPantry objects with same user and
        ingredient raises IntegrityError.
        """
        get_ing_in_pantry()
        with self.assertRaises(IntegrityError):
            get_ing_in_pantry(quantity=200, measurement_unit='g')

    def test_delete_unused_ingredient(self):
        """
        Test that deleting ingredient in pantry also deletes ingredient if it
        is unused by other entities.
        """
        ing = Ingredient.objects.create(name='ing name')
        ing_id = ing.id
        ing_in_pantry = get_ing_in_pantry(ingredient=ing)
        ing_in_pantry.delete()

        self.assertFalse(Ingredient.objects.filter(id=ing_id).exists())

    def test_delete_ing_pantry_with_used_ingredient(self):
        """
        Test that deleting inggredient in pantry does not delete ingredient
        if it is used by another entity.
        """
        another_user = create_user(email='another_user@example.com')
        ing = Ingredient.objects.create(name='ing name')
        ing_id = ing.id
        ing_in_pantry_1 = get_ing_in_pantry(ingredient=ing)
        ing_in_pantry_2 = get_ing_in_pantry(
            user=another_user,
            ingredient=ing
        )
        ing_in_pantry_1.delete()

        # Ingredient used by ing_in-pantry_2
        self.assertTrue(Ingredient.objects.filter(id=ing_id).exists())

        recipe = Recipe.objects.create(
            user=another_user,
            title='a recipe',
            directions=['step 1']
        )
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ing)
        ing_in_pantry_2.delete()

        # Ingredient used by a recipe ingredient
        self.assertTrue(Ingredient.objects.filter(id=ing_id).exists())

    def test_subtract_quantity(self):
        """
        Test that subtract_quantity succeeds in subtracting from quantity.
        """
        original_quantity = 100
        ing_in_pantry = get_ing_in_pantry(quantity=original_quantity)
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
        ing_in_pantry = get_ing_in_pantry()
        sub_quantity = ing_in_pantry.quantity + 1
        ing_in_pantry.subtract_quantity(
            sub_quantity, ing_in_pantry.measurement_unit)

        self.assertEqual(ing_in_pantry.quantity, 0)

    def test_subtract_with_wrong_unit(self):
        """
        Test that calling subtract_quantity with a mismatched unit raises a
        ValueError.
        """
        ing_in_pantry = get_ing_in_pantry(measurement_unit='g')
        with self.assertRaises(ValueError):
            ing_in_pantry.subtract_quantity(50, 'ml')


class RecipeIngredientModelTests(TestCase):
    """Tests for the RecipeIngredient model."""

    def test_add_ingredient_to_recipe(self):
        """Test creating RecipeIngredient instance."""
        recipe = Recipe.objects.create(
            user=create_user(),
            title='title',
            directions=['step 1']
        )
        ing = Ingredient.objects.create(name='ing')
        recipe_ing = RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=ing,
            quantity=473.18,
            measurement_unit='ml',
            display_unit='cup'
        )
        self.assertEqual(str(recipe_ing), f'{str(ing)} in {str(recipe)}')
