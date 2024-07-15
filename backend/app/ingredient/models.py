"""
Ingredient app models.
"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.constraints import UniqueConstraint

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


class IngredientManagementBase(models.Model):
    """Base model for ingredients in different contexts."""
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=9, default=0, decimal_places=2)
    measurement_unit = models.CharField(
        max_length=3,
        choices=MeasurementUnits.choices,
        default=MeasurementUnits.UNIT
    )
    display_unit = models.CharField(max_length=20)

    _ingredient_management_models = []

    class Meta:
        abstract = True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        IngredientManagementBase._ingredient_management_models.append(cls)

    @classmethod
    def create_with_display_unit(cls, **kwargs):
        """
        Create an instance with quantity in display unit.
        measurement_unit used internally and converted quantity are set
        accordingly.
        """
        display_unit = kwargs.get('display_unit')
        quantity = kwargs.pop('quantity')
        if display_unit not in DISPLAY_UNITS:
            raise ValidationError('Invalid display_unit.')

        measurement_unit = DISPLAY_UNITS[display_unit].get_standard_unit()
        converted_quantity = DISPLAY_UNITS[display_unit].convert_quantity(
            quantity)

        return cls.objects.create(
            measurement_unit=measurement_unit,
            quantity=converted_quantity,
            **kwargs
            )

    def add_quantity(self, quantity_to_add, unit):
        """
        Add quantity of ingredient.
        - ValueError is raised if this method is called with a measurement
        unit different from the one of the object or if the quantity of the
        object has not been set.
        """
        if self.quantity is None:
            raise ValueError("Quantity not set for this ingredient.")
        if quantity_to_add < 0:
            raise ValueError("This method should be called with a positive\
                              value for quantity.")
        if self.measurement_unit == unit:
            self.quantity = self.quantity + quantity_to_add
        else:
            unit_name = MeasurementUnits(self.measurement_unit).label
            raise ValueError(f'Cannot add quantity with different '
                             f'measurement units. Convert the add '
                             f'quantity to {unit_name}'
                             f'({self.measurement_unit})')
        self.save()
        return self.quantity

    def delete(self):
        """
        Delete self and associated Ingredient instace if it is not associated
        with any other instance.
        """
        ingredient = self.ingredient
        super().delete()
        subclasses = self.__class__._ingredient_management_models
        used = False
        for subclass in subclasses:
            if subclass.objects.filter(ingredient=ingredient).exists():
                used = True
                break
        if not used:
            ingredient.delete()

    def get_display_quantity(self):
        """Get quantity in display unit."""
        return DISPLAY_UNITS[self.display_unit].convert_to_display_unit(
            self.quantity)

    def subtract_quantity(self, sub_quantity, sub_unit):
        """
        Subtract quantity of ingredient.
        - If subtracted quantity is greater or equal to the ingredient's
        quantity the instance is deleted.
        - ValueError is raised if this method is called with a measurement
        unit different from the one of the object or if the quantity of the
        object has not been set.
        """
        if self.quantity is None:
            raise ValueError("Quantity not set for this ingredient.")
        if self.measurement_unit == sub_unit:
            self.quantity = self.quantity - sub_quantity
        else:
            unit_name = MeasurementUnits(self.measurement_unit).label
            raise ValueError(f'Cannot subtract quantity with different '
                             f'measurement units. Convert the subtract '
                             f'quantity to {unit_name}'
                             f'({self.measurement_unit})')
        if self.quantity <= 0:
            self.delete()
        else:
            self.save()

        return self.quantity


class IngredientInPantry(IngredientManagementBase):
    """Ingrendient a user has."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expiration = models.DateField(null=True, default=None)
    quantity = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, default=None)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'ingredient'],
                name='unique_pantry_ingredient'
                )
            ]

    def __str__(self):
        return f'{self.ingredient.name} - {self.user.email}'


class RecipeIngredient(IngredientManagementBase):
    """Ingredient in a recipe."""
    recipe = models.ForeignKey('recipe.Recipe', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
                )
            ]

    def __str__(self):
        return f'{str(self.ingredient)} in {str(self.recipe)}'


class ShoppingListItem(IngredientManagementBase):
    """Item of user's shopping list."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'ingredient'],
                name='unique_shopping_list_item'
                )
            ]

    def __str__(self):
        return f'{str(self.ingredient)} in {str(self.user)}\'s shopping list.'
