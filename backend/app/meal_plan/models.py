"""Models for the meal_plan app."""

from django.contrib.auth import get_user_model
from django.db import models

from ingredient.models import IngredientInPantry, RecipeIngredient

User = get_user_model()


class Preferences(models.Model):
    """General user's preferences for meal plans."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    servings_per_meal = models.PositiveSmallIntegerField(null=True)
    cookings_per_week = models.PositiveSmallIntegerField(null=True)


class Meal(models.Model):
    """A meal composed by a main dish, a side dish, and a salad."""
    meal_plan = models.ForeignKey('MealPlan', on_delete=models.CASCADE)
    day = models.PositiveSmallIntegerField()
    main_dish = models.ForeignKey(
        'recipe.Recipe',
        on_delete=models.CASCADE,
        related_name='main_dish',
        null=True,
        default=None
        )
    side_dish = models.ForeignKey(
        'recipe.Recipe',
        on_delete=models.CASCADE,
        related_name='side_dish',
        null=True,
        default=None
        )
    salad = models.ForeignKey(
        'recipe.Recipe',
        on_delete=models.CASCADE,
        related_name='salad',
        null=True,
        default=None
        )

    def subtract_from_pantry(self, servings_per_meal):
        """Subtract the quantity of ingredients in meal from pantry."""
        for recipe in ('main_dish', 'side_dish', 'salad'):
            recipe_ings = RecipeIngredient.objects.filter(
                recipe=getattr(self, recipe))
            for recipe_ing in recipe_ings:
                ingredient = recipe_ing.ingredient
                if (IngredientInPantry.objects.filter(
                        ingredient=ingredient).exists()):
                    ing_pantry = IngredientInPantry.objects.get(
                        ingredient=ingredient)
                    ing_pantry.subtract_quantity(
                        sub_quantity=recipe_ing.quantity * servings_per_meal,
                        sub_unit=recipe_ing.measurement_unit
                        )


class MealPlan(models.Model):
    """User's meal plan for the week."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    servings_per_meal = models.PositiveSmallIntegerField(default=2)
    creation_date = models.DateField(auto_now_add=True)

    def subtract_from_pantry(self):
        """Subtract the quantity of ingredients in meal plan from pantry."""
        meals = Meal.objects.filter(meal_plan=self)
        for meal in meals:
            meal.subtract_from_pantry(self.servings_per_meal)
