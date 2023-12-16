"""
API views for the ingredient app.
"""

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError
from typing import List

from ingredient.models import IngredientInPantry
from ingredient.schemas import PantryListSchema, PantryDetailSchema

pantry_router = Router()


@pantry_router.get('/', response=List[PantryListSchema],
                   url_name='pantry_list')
def pantry_list(request):
    """Retrieves all user's ingredients in pantry."""
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


@pantry_router.get('/{ing_pantry_id}', response=PantryDetailSchema,
                   url_name='pantry_detail')
def pantry_detail(request, ing_pantry_id: int):
    """Retrieves details of an ingriendt in pantry."""
    user = request.auth
    ing_pantry = get_object_or_404(IngredientInPantry, id=ing_pantry_id)
    if ing_pantry.user != user:
        raise HttpError(401, "Unauthorized")
    response = {
        'name': ing_pantry.ingredient.name,
        'quantity': ing_pantry.quantity,
        'measurement_unit': ing_pantry.measurement_unit,
        'expiration': ing_pantry.expiration
    }
    return response
