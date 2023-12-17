"""
Utility functions for the the ingredient app API.
"""

from django.shortcuts import get_object_or_404
from ninja.errors import HttpError

from ingredient.models import Ingredient, IngredientInPantry


def get_ing_pantry_detail(ing_pantry_id: int, user):
    """
    Return ing_in_pantry if it belongs to user.
    """
    ing_pantry = get_object_or_404(IngredientInPantry, id=ing_pantry_id)
    if ing_pantry.user != user:
        raise HttpError(401, "Unauthorized")
    return ing_pantry


def get_or_create_ingredient(ing_name, user):
    """Get or create an ingredient and return it."""
    # get or create ingredient in the system
    ing, ing_created = Ingredient.objects.get_or_create(name=ing_name)
    # set added_by field to user if it was created
    if ing_created:
        ing.added_by = user
        ing.save()
    return ing


def response_ing_in_pantry(ing_pantry):
    """Response of an ingredient in pantry."""
    return {
        'id': ing_pantry.id,
        'name': ing_pantry.ingredient.name,
        'quantity': ing_pantry.quantity,
        'measurement_unit': ing_pantry.measurement_unit,
        'expiration': ing_pantry.expiration
    }
