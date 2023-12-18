"""
Ingredient app models.
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from recipe.models import Recipe

User = get_user_model()


class MeasurementUnits(models.TextChoices):
    GRAM = 'g', _('gram')
    MILLILITER = 'ml', _('milliliter')
    UNIT = 'un', _('unit')


class Ingredient(models.Model):
    """Ingredient in the system."""
    name = models.CharField(max_length=63, unique=True)
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        default=None
    )

    def __str__(self):
        return self.name


class IngredientInPantry(models.Model):
    """Ingrendient a user has."""
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    quantity = models.DecimalField(max_digits=6, default=0, decimal_places=2)
    measurement_unit = models.CharField(
        max_length=3,
        choices=MeasurementUnits.choices,
        default=MeasurementUnits.UNIT
    )
    expiration = models.DateField(null=True, default=None)

    class Meta:
        unique_together = ['user', 'ingredient']

    def delete(self):
        """
        Delete IngredientInPantry instance and Ingredient if it is not
        associated with other IngredientInPantry or RecipeIngredient.
        """
        ingredient = self.ingredient
        super().delete()
        ing_pantry_exists = IngredientInPantry.objects.filter(
            ingredient=ingredient).exists()
        recipe_ing_exists = RecipeIngredient.objects.filter(
            ingredient=ingredient).exists()
        if not ing_pantry_exists and not recipe_ing_exists:
            ingredient.delete()

    def subtract_quantity(self, sub_quantity, sub_unit):
        """
        Subtracts quantity of ingredient.
        If subtracted quantity is greater, quantity is set to 0.
        Convert the value of value to be subtracted to the same used in this
        object.
        """
        if self.measurement_unit == sub_unit:
            self.quantity = max(0, self.quantity - sub_quantity)
        else:
            unit_name = MeasurementUnits(self.measurement_unit).label
            raise ValueError(f'Cannot subtract quantity with different'
                             f'measurement units. Convert the subtract'
                             f'quantity to {unit_name}'
                             f'({self.measurement_unit})')
        return self.quantity

    def __str__(self):
        return f'{self.ingredient.name} - {self.user.email}'


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
