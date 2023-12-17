"""
API views for the ingredient app.
"""

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError
from typing import List

from ingredient.models import Ingredient, IngredientInPantry
from ingredient.schemas import (
    PantryListSchema,
    PantryDetailIn,
    PantryDetailOut,
    PantryDetailPatch
    )

pantry_router = Router()


def get_ing_pantry_detail(ing_pantry_id: int, user):
    """
    Return ing_in_pantry if it belongs to user.
    """
    ing_pantry = get_object_or_404(IngredientInPantry, id=ing_pantry_id)
    if ing_pantry.user != user:
        raise HttpError(401, "Unauthorized")
    return ing_pantry


def response_ing_in_pantry(ing_pantry):
    """Response of an ingredient in pantry."""
    return {
        'id': ing_pantry.id,
        'name': ing_pantry.ingredient.name,
        'quantity': ing_pantry.quantity,
        'measurement_unit': ing_pantry.measurement_unit,
        'expiration': ing_pantry.expiration
    }


def get_or_create_ingredient(ing_name, user):
    """Get or create an ingredient and return it."""
    # get or create ingredient in the system
    ing, ing_created = Ingredient.objects.get_or_create(name=ing_name)
    # set added_by field to user if it was created
    if ing_created:
        ing.added_by = user
        ing.save()
    return ing


@pantry_router.get('/', response=List[PantryListSchema],
                   url_name='pantry_list')
def pantry_list(request):
    """Retrieve all user's ingredients in pantry."""
    user = request.auth
    queryset = (IngredientInPantry.objects
                .filter(user=user)
                .order_by('ingredient__name'))
    response = list()
    for ing_pantry in queryset:
        response.append({
            'id': ing_pantry.id,
            'name': ing_pantry.ingredient.name
        })
    return response


@pantry_router.post('/', response={201: PantryDetailOut})
def add_ing_to_pantry(request, payload: PantryDetailIn):
    """Add ingredient to user's pantry."""
    user = request.auth
    ing_pantry_data = payload.dict()
    name = ing_pantry_data.pop('name')
    ing = get_or_create_ingredient(name, user)
    ing_pantry_data['ingredient'] = ing
    ing_pantry_data['user'] = user
    ing_pantry = IngredientInPantry.objects.create(**ing_pantry_data)
    return 201, response_ing_in_pantry(ing_pantry)


@pantry_router.get('/{ing_pantry_id}', response=PantryDetailOut,
                   url_name='pantry_detail')
def pantry_detail(request, ing_pantry_id: int):
    """Retrieve details of an ingriendt in pantry."""
    ing_pantry = get_ing_pantry_detail(ing_pantry_id, user=request.auth)
    return response_ing_in_pantry(ing_pantry)


@pantry_router.patch('/{ing_pantry_id}', response=PantryDetailOut)
def pantry_update(request, ing_pantry_id: int, payload: PantryDetailPatch):
    """Updates ingredient in pantry."""
    ing_pantry = get_ing_pantry_detail(ing_pantry_id, user=request.auth)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr == 'name':
            # update ingredient name or create a new one.
            ing = get_or_create_ingredient(
                ing_pantry.ingredient.name, user=request.auth)
            ing_pantry.ingredient = ing
            ing.name = value
            ing.save()
        setattr(ing_pantry, attr, value)
    ing_pantry.save()
    return response_ing_in_pantry(ing_pantry)


@pantry_router.delete('/{ing_pantry_id}', response={204: None})
def pantry_delete(request, ing_pantry_id: int):
    ing_pantry = get_ing_pantry_detail(ing_pantry_id, user=request.auth)
    ing_pantry.delete()
    return 204, None
