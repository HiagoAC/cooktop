"""
Tests for ingredient app models.
"""

from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from app.utils_test import (
    create_ing_in_pantry,
    create_shopping_list_item,
    create_user
)
from ingredient.measurement_units import DISPLAY_UNITS, MeasurementUnits
from ingredient.models import (
    Ingredient,
    IngredientInPantry,
    RecipeIngredient
)
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

    def setUp(self):
        self.user = create_user()

    def test_create_ing_in_pantry_same_user_and_ingredient(self):
        """
        Test that creating two IngredientInPantry objects with same user and
        ingredient raises IntegrityError.
        """
        create_ing_in_pantry(user=self.user)
        with self.assertRaises(IntegrityError):
            create_ing_in_pantry(
                user=self.user, quantity=200, display_unit='gram')

    def test_add_quantity_measurement_unit(self):
        """
        Test adding to quantity with ingredient's measurement unit with
        add_quantity.
        """
        original_quantity = 100
        ingredient, _ = Ingredient.objects.get_or_create(name='a food')
        ing_pantry = IngredientInPantry.objects.create(
            user=self.user,
            ingredient=ingredient,
            quantity=original_quantity,
            measurement_unit=MeasurementUnits.GRAM
        )
        add_quantity = 50
        ing_pantry.add_quantity(add_quantity, ing_pantry.measurement_unit)

        self.assertEqual(
            ing_pantry.quantity, original_quantity + add_quantity)

    def test_add_quantity_with_convertable_unit(self):
        """
        Test adding to quantity with a convertable unit.
        """
        original_quantity = 100
        ingredient, _ = Ingredient.objects.get_or_create(name='a food')
        ing_pantry = IngredientInPantry.objects.create(
            user=self.user,
            ingredient=ingredient,
            quantity=original_quantity,
            measurement_unit='ml'
        )
        add_quantity = 2
        ing_pantry.add_quantity(add_quantity, 'cup')
        add_quantity_ml = DISPLAY_UNITS['cup'].convert_quantity(add_quantity)

        self.assertEqual(
            ing_pantry.quantity, original_quantity + add_quantity_ml)

    def test_add_quantity_with_wrong_unit(self):
        """
        Test adding to quantity with a wrong unit raises a ValueError.
        """
        ing_pantry = create_ing_in_pantry(
            user=self.user,
            display_unit='gram',
            quantity=100
        )
        with self.assertRaises(ValueError):
            ing_pantry.add_quantity(50, 'ml')

    def test_delete_ing_in_pantry_with_unused_ingredient(self):
        """
        Test that deleting ingredient in pantry also deletes ingredient if it
        is unused by other entities.
        """
        ing_in_pantry = create_ing_in_pantry(user=self.user)
        ing_id = ing_in_pantry.ingredient.id
        ing_in_pantry.delete()

        self.assertFalse(Ingredient.objects.filter(id=ing_id).exists())

    def test_delete_ing_pantry_with_used_ingredient(self):
        """
        Test that deleting ingredient in pantry does not delete ingredient
        if it is used by another entity.
        """
        another_user = create_user(email='another_user@example.com')
        ing_name = 'ing name'
        ing_in_pantry_1 = create_ing_in_pantry(user=self.user, name=ing_name)
        ing = ing_in_pantry_1.ingredient
        ing_in_pantry_2 = create_ing_in_pantry(
            user=another_user,
            name=ing_name
        )
        ing_in_pantry_1.delete()

        # Ingredient used by ing_in-pantry_2
        self.assertTrue(Ingredient.objects.filter(id=ing.id).exists())

        recipe = Recipe.objects.create(
            user=another_user,
            title='a recipe',
            directions=['step 1']
        )
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ing)
        ing_in_pantry_2.delete()

        # Ingredient used by a recipe ingredient
        self.assertTrue(Ingredient.objects.filter(id=ing.id).exists())

    def test_subtract_quantity(self):
        """
        Test that subtract_quantity succeeds in subtracting from quantity.
        """
        original_quantity = 100
        ingredient, _ = Ingredient.objects.get_or_create(name='a food')
        ing_in_pantry = IngredientInPantry.objects.create(
            user=self.user,
            ingredient=ingredient,
            quantity=original_quantity,
            measurement_unit='ml'
        )
        sub_quantity = 50
        ing_in_pantry.subtract_quantity(
            sub_quantity, ing_in_pantry.measurement_unit)

        self.assertEqual(
            ing_in_pantry.quantity, original_quantity - sub_quantity)

    def test_subtract_all_quantity(self):
        """
        Test that subtracting all quantity of ingredient in pantry makes it to
        be deleted.
        """
        ing_in_pantry = create_ing_in_pantry(user=self.user)
        ing_in_pantry.subtract_quantity(
            ing_in_pantry.quantity, ing_in_pantry.measurement_unit)

        self.assertFalse(
            IngredientInPantry.objects.filter(id=ing_in_pantry.id).exists())

    def test_subtract_when_quantity_not_set(self):
        """
        Test that subtracting when quantity is not set raises a ValueError.
        """
        ingredient, _ = Ingredient.objects.get_or_create(name='a food')
        ing_in_pantry = IngredientInPantry.objects.create(
            user=self.user, ingredient=ingredient)
        with self.assertRaises(ValueError):
            ing_in_pantry.subtract_quantity(50, 'ml')

    def test_subtract_with_convertable_unit(self):
        """
        Test that subtracting with a convertable unit works.
        """
        original_quantity = 1000
        ingredient, _ = Ingredient.objects.get_or_create(name='a food')
        ing_in_pantry = IngredientInPantry.objects.create(
            user=self.user,
            ingredient=ingredient,
            quantity=original_quantity,
            measurement_unit='ml'
        )
        sub_quantity = 2
        ing_in_pantry.subtract_quantity(sub_quantity, 'cup')
        sub_quantity_ml = DISPLAY_UNITS['cup'].convert_quantity(sub_quantity)

        self.assertEqual(
            ing_in_pantry.quantity, original_quantity - sub_quantity_ml)

    def test_subtract_with_wrong_unit(self):
        """
        Test that calling subtract_quantity with a mismatched unit raises a
        ValueError.
        """
        ing_in_pantry = create_ing_in_pantry(
            user=self.user, display_unit='gram')
        with self.assertRaises(ValueError):
            ing_in_pantry.subtract_quantity(50, 'ml')


class RecipeIngredientModelTests(TestCase):
    """Tests for the RecipeIngredient model."""

    def setUp(self):
        self.user = create_user()
        self.recipe = Recipe.objects.create(
            user=self.user,
            title='title',
            directions=['step 1']
        )
        self.ing = Ingredient.objects.create(name='ing')

    def test_add_ingredient_to_recipe(self):
        """Test creating RecipeIngredient instance."""
        recipe_ing = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ing,
            quantity=473.18,
            measurement_unit='ml',
            display_unit='cup'
        )

        self.assertEqual(
            str(recipe_ing), f'{str(self.ing)} in {str(self.recipe)}')

    def test_create_recipe_ingredient_with_display_unit(self):
        """
        Test creating a recipe_ingredient with method
        create_with_display_units.
        """
        recipe_ing = RecipeIngredient.create_with_display_unit(
            recipe=self.recipe,
            ingredient=self.ing,
            quantity=2,
            display_unit='cup'
        )

        self.assertEqual(recipe_ing.quantity, Decimal('473.18'))
        self.assertEqual(recipe_ing.measurement_unit,
                         MeasurementUnits.MILLILITER)

    def test_delete_recipe_ingredient_with_unused_ingredient(self):
        """
        Test that deleting recipe_ingredient also deletes ingredient if it
        is unused by other entities.
        """
        ing = Ingredient.objects.create(name='another ing')
        ing_id = ing.id
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe, ingredient=ing)
        recipe_ingredient.delete()

        self.assertFalse(Ingredient.objects.filter(id=ing_id).exists())

    def test_delete_recipe_ingredient_with_used_ingredient(self):
        """
        Test that deleting recipe_ingredient does not delete ingredient
        if it is used by another entity.
        """
        user = create_user(email='another_user@example.com')
        ing_name = 'another ing'
        ing = Ingredient.objects.create(name=ing_name)
        rec_1 = Recipe.objects.create(
            user=user, title='a recipe', directions=['step 1'])
        rec_ing_1 = RecipeIngredient.objects.create(
            recipe=rec_1, ingredient=ing)
        rec_2 = Recipe.objects.create(
            user=user, title='recipe 2', directions=['step 1'])
        rec_ing_2 = RecipeIngredient.objects.create(
            recipe=rec_2, ingredient=ing)
        rec_ing_1.delete()

        # Ingredient used by rec_ing_2
        self.assertTrue(Ingredient.objects.filter(id=ing.id).exists())

        create_ing_in_pantry(user=self.user, name=ing_name)
        rec_ing_2.delete()

        # Ingredient used by an ingredient_in_pantry
        self.assertTrue(Ingredient.objects.filter(id=ing.id).exists())


class ShoppingListItemModelTests(TestCase):
    """Tests for the ShoppingListItem model."""

    def setUp(self):
        self.user = create_user()

    def test_create_shopping_list_item_same_user_and_ingredient(self):
        """
        Test that creating two ShoppingListItem objects with same user and
        ingredient raises IntegrityError.
        """
        create_shopping_list_item(user=self.user)
        with self.assertRaises(IntegrityError):
            create_shopping_list_item(
                user=self.user, quantity=200, display_unit='gram')
