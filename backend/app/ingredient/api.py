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
    PantryDetailOut
    )

pantry_router = Router()


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
    # get or create ingredient in the system
    ing, ing_created = Ingredient.objects.get_or_create(name=name)
    # set added_by field to user if it was created
    if ing_created:
        ing.added_by = user
        ing.save()
    ing_pantry_data['ingredient'] = ing
    ing_pantry_data['user'] = user
    ing_pantry = IngredientInPantry.objects.create(**ing_pantry_data)
    response = {
        'id': ing_pantry.pk,
        'name': name,
        'quantity': ing_pantry.quantity,
        'measurement_unit': ing_pantry.measurement_unit,
        'expiration': ing_pantry.expiration
    }
    return 201, response


@pantry_router.get('/{ing_pantry_id}', response=PantryDetailOut,
                   url_name='pantry_detail')
def pantry_detail(request, ing_pantry_id: int):
    """Retrieve details of an ingriendt in pantry."""
    user = request.auth
    ing_pantry = get_object_or_404(IngredientInPantry, id=ing_pantry_id)
    if ing_pantry.user != user:
        raise HttpError(401, "Unauthorized")
    response = {
        'id': ing_pantry_id,
        'name': ing_pantry.ingredient.name,
        'quantity': ing_pantry.quantity,
        'measurement_unit': ing_pantry.measurement_unit,
        'expiration': ing_pantry.expiration
    }
    return response
