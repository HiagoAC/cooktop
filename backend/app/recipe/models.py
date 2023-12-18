"""
Recipe app models.
"""

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models

from ingredient.models import Ingredient, MeasurementUnits

User = get_user_model()


class Recipe(models.Model):
    """Recipe of a user."""
    # required
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    directions = ArrayField(models.TextField(max_length=1023))

    # optional
    description = models.TextField(blank=True)
    servings = models.PositiveSmallIntegerField(null=True, default=None)
    time_minutes = models.PositiveSmallIntegerField(null=True, default=None)
    notes = models.TextField(blank=True)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    """Ingredient in a recipe."""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, default=0, decimal_places=2)
    measurement_unit = models.CharField(
        max_length=3,
        choices=MeasurementUnits.choices,
        default=MeasurementUnits.UNIT
    )
    display_unit = models.CharField(max_length=20)

    def __str__(self):
        return f'{str(self.ingredient)} in {str(self.recipe)}'


class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=63)
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        default=None
    )

    def __str__(self):
        return self.name
