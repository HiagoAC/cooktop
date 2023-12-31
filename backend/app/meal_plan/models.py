"""Models for the meal_plan app."""

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Preferences(models.Model):
    """General user's preferences for meal plans."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    servings_per_meal = models.PositiveSmallIntegerField(null=True)
    cookings_per_week = models.PositiveSmallIntegerField(null=True)


class Meal(models.Model):
    """A meal composed by a main dish, a side dish, and a salad."""
    main_dish = models.ForeignKey(
        'recipe.Recipe',
        on_delete=models.CASCADE,
        related_name='main_dish',
        null=True
        )
    side_dish = models.ForeignKey(
        'recipe.Recipe',
        on_delete=models.CASCADE,
        related_name='side_dish',
        null=True
        )
    salad = models.ForeignKey(
        'recipe.Recipe',
        on_delete=models.CASCADE,
        related_name='salad',
        null=True
        )
    day = models.PositiveSmallIntegerField()


class MealPlan(models.Model):
    """User's meal plan for the week."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meals = models.ManyToManyField('Meal')
    servings_per_meal = models.PositiveSmallIntegerField(default=2)
    creation_date = models.DateTimeField(auto_now_add=True)
