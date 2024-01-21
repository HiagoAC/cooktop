"""Tests for models in the meal_plan app."""

from django.test import TestCase

from app.utils_test import (
    create_ing_in_pantry,
    create_meal,
    create_recipe,
    create_recipe_ing,
    create_user
)
from ingredient.models import IngredientInPantry
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
            'meal_plan': MealPlan.objects.create(user=user),
            'day': 1,
            'main_dish': create_recipe(
                user=user, recipe_type=Recipe.RecipeTypes.MAIN_DISH),
            'side_dish': create_recipe(
                user=user, recipe_type=Recipe.RecipeTypes.SIDE_DISH),
            'salad': create_recipe(
                user=user, recipe_type=Recipe.RecipeTypes.SALAD),
        }
        meal = Meal.objects.create(**params)

        for attr, value in params.items():
            self.assertEqual(getattr(meal, attr), value)


class MealPlanModelTests(TestCase):
    """Tests for the MealPlan model."""

    def setUp(self):
        self.user = create_user()
        self.meal_plan = MealPlan.objects.create(user=self.user)

    def test_create_meal_plan(self):
        """Test creating a meal_plan."""
        servings_per_meal = 2
        meal_plan = MealPlan.objects.create(
            user=self.user, servings_per_meal=servings_per_meal)

        self.assertEqual(servings_per_meal, meal_plan.servings_per_meal)

    def test_subtract_from_pantry(self):
        """Test subtracting ingredients of meal plan from pantry."""
        main_dish = create_recipe(
            user=self.user, recipe_type=Recipe.RecipeTypes.MAIN_DISH)
        side_dish = create_recipe(
            user=self.user, recipe_type=Recipe.RecipeTypes.SIDE_DISH)
        # Ingredient in pantry. Quantity in pantry enough
        ing_1 = create_ing_in_pantry(
            name='ing 1', quantity=100, measurement_unit='ml', user=self.user)
        rec1_ing1 = create_recipe_ing(
            recipe=main_dish,
            name=ing_1.ingredient.name,
            quantity=10,
            display_unit='ml'
            )
        rec2_ing2 = create_recipe_ing(
            recipe=side_dish,
            name=ing_1.ingredient.name,
            quantity=30,
            display_unit='ml'
            )
        final_quant_ing_1 = ing_1.quantity - \
            ((rec1_ing1.quantity + rec2_ing2.quantity) *
             self.meal_plan.servings_per_meal)
        # Ingredient not in pantry
        create_recipe_ing(
            recipe=main_dish, name='ing_2', quantity=50, display_unit='ml')

        create_meal(
            meal_plan=self.meal_plan,
            day=1,
            main_dish=main_dish
            )
        create_meal(
            meal_plan=self.meal_plan,
            day=2,
            side_dish=side_dish
            )

        self.meal_plan.subtract_from_pantry()
        ing_1.refresh_from_db()

        self.assertEqual(ing_1.quantity, final_quant_ing_1)

    def test_subtract_from_pantry_not_enough(self):
        """
        Test subtracting ingredients of meal plan from pantry when quantity of
        ingredients in meal plan is greater than the quantity in pantry.
        """
        main_dish = create_recipe(
            user=self.user, recipe_type=Recipe.RecipeTypes.MAIN_DISH)
        # Ingredient in pantry. Quantity in pantry not enough (2 servings=102)
        ing_pantry = create_ing_in_pantry(
            name='ing', quantity=50, measurement_unit='ml', user=self.user)
        ing_pantry_id = ing_pantry.id
        create_recipe_ing(
            recipe=main_dish,
            name=ing_pantry.ingredient.name,
            quantity=26,
            display_unit='ml'
            )
        create_meal(
            meal_plan=self.meal_plan,
            day=1,
            main_dish=main_dish
            )
        self.meal_plan.subtract_from_pantry()

        self.assertFalse(IngredientInPantry.objects.filter(
            id=ing_pantry_id).exists())
