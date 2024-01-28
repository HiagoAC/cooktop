"""
API views for the ingredient app.
"""

from ninja import Router
from typing import List

from app.utils_api import get_instance_detail
from ingredient.measurement_units import DISPLAY_UNITS
from ingredient.api_utils import (
    get_ing_pantry_detail,
    get_or_create_ingredient,
    response_ing_in_pantry
    )
from ingredient.models import IngredientInPantry, ShoppingListItem
from ingredient.schemas import (
    PantryListSchema,
    PantryDetailIn,
    PantryDetailOut,
    PantryDetailPatch,
    ShoppingListItemIn,
    ShoppingListItemOut,
    ShoppingListItemPatch
    )

pantry_router = Router()
shopping_list_router = Router()


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
    """Update ingredient in pantry."""
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


@shopping_list_router.get('/', response=List[ShoppingListItemOut],
                          url_name='shopping_list')
def shopping_list(request):
    """Retrieve user's shopping list."""
    user = request.auth
    queryset = (ShoppingListItem.objects
                .filter(user=user)
                .order_by('ingredient__name'))
    return list(queryset)


@shopping_list_router.get('/{item_id}', response=ShoppingListItemOut,
                          url_name='shopping_item_detail')
def shopping_item_detail(request, item_id: int):
    """Retrieve details of shopping list item."""
    item = get_instance_detail(item_id, ShoppingListItem, user=request.auth)
    return item


@shopping_list_router.post('/', response={201: ShoppingListItemOut})
def add_item_to_shopping_list(request, payload: ShoppingListItemIn):
    """Add ingredient to user's shopping list."""
    user = request.auth
    item_data = payload.dict()
    name = item_data.pop('name')
    ing = get_or_create_ingredient(name, user)
    item_data['ingredient'] = ing
    item_data['user'] = user
    item_data['display_unit'] = item_data.pop('unit')
    item = ShoppingListItem.create_with_display_unit(**item_data)
    return 201, item


@shopping_list_router.patch('/{item_id}', response=ShoppingListItemOut)
def shopping_list_update(
        request, item_id: int, payload: ShoppingListItemPatch):
    """Update ingredient in user's shopping list."""
    item = get_instance_detail(item_id, ShoppingListItem, user=request.auth)
    upload_data = payload.dict(exclude_unset=True)
    if 'name' in upload_data:
        ing = get_or_create_ingredient(
            item.ingredient.name, user=request.auth)
        item.ingredient = ing
        ing.name = upload_data['name']
        ing.save()
    if 'unit' in upload_data:
        item.display_unit = upload_data['unit']
        item.measurement_unit = DISPLAY_UNITS[
            upload_data['unit']].get_standard_unit()
    if 'quantity' in upload_data:
        item.quantity = DISPLAY_UNITS[
            upload_data['unit']].convert_quantity(upload_data['quantity'])
    item.save()
    return item
