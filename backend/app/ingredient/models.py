"""
Ingredient app models.
"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from ingredient.measurement_units import DISPLAY_UNITS, MeasurementUnits

User = get_user_model()


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
        associated with another IngredientInPantry or RecipeIngredient
        instance.
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
    recipe = models.ForeignKey('recipe.Recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, default=0, decimal_places=2)
    measurement_unit = models.CharField(
        max_length=3,
        choices=MeasurementUnits.choices,
        default=MeasurementUnits.UNIT
    )
    display_unit = models.CharField(max_length=20)

    @classmethod
    def create_with_display_unit(cls, recipe, ingredient, display_unit,
                                 quantity):
        """
        Create an instance of RecipeIngredient with quantity in display unit.
        Use this method instead of RecipeIngredient.objects.create().
        measurement_unit used internally and converted quantity are set
        accordingly.
        """
        if display_unit not in DISPLAY_UNITS:
            raise ValidationError('Invalid display_unit.')

        measurement_unit = DISPLAY_UNITS[display_unit].get_standard_unit()
        quantity = DISPLAY_UNITS[display_unit].convert_quantity(quantity)

        return cls.objects.create(
            recipe=recipe,
            ingredient=ingredient,
            quantity=quantity,
            measurement_unit=measurement_unit,
            display_unit=display_unit
        )

    def get_display_quantity(self):
        """Get quantity in display unit."""
        return DISPLAY_UNITS[self.display_unit].convert_to_display_unit(
            self.quantity)

    def delete(self):
        """
        Delete RecipeIngredient instance and Ingredient if it is not
        associated with another IngredientInPantry or RecipeIngredient
        instance.
        """
        ingredient = self.ingredient
        super().delete()
        ing_pantry_exists = IngredientInPantry.objects.filter(
            ingredient=ingredient).exists()
        recipe_ing_exists = RecipeIngredient.objects.filter(
            ingredient=ingredient).exists()
        if not ing_pantry_exists and not recipe_ing_exists:
            ingredient.delete()

    def __str__(self):
        return f'{str(self.ingredient)} in {str(self.recipe)}'
