"""
Utitility functions for ingredient app tests.
"""

from django.contrib.auth import get_user_model
from ingredient.models import Ingredient, IngredientInPantry


User = get_user_model()


def get_ing_in_pantry(quantity=100, measurement_unit='ml',
                        user=None, ingredient=None):
    """Returns an instance of IngredientInPantry."""
    if not user:
        user = User.objects.create_user(
            email='email@example.com', password='password321')
    if not ingredient:
        ingredient = Ingredient.objects.create(name='food name')
    ing_in_pantry = IngredientInPantry.objects.create(
        user=user,
        ingredient=ingredient,
        quantity=quantity,
        measurement_unit=measurement_unit
    )
    return ing_in_pantry
