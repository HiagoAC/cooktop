"""
API views for the ingredient app.
"""

from ninja import Router
from typing import List

from ingredient.models import IngredientInPantry
from ingredient.schemas import PantryListSchema

pantry_router = Router()


@pantry_router.get('/', response=List[PantryListSchema],
                   url_name='pantry_list')
def pantry_list(request):
    """Retrieves all user's ingredients in pantry."""
    user = request.auth
    query = (IngredientInPantry.objects
             .filter(user=user)
             .order_by('ingredient__name'))
    response = list()
    for ing_pantry in query:
        response.append({
            'id': ing_pantry.id,
            'name': ing_pantry.ingredient.name
        })
    return response


@pantry_router.get('/{ing_pantry_id}', response=None, url_name='pantry_detail')
def pantry_detail(request, ing_pantry_id: int):
    """Retrieves details of an ingriendt in pantry."""
    pass
