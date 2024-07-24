"""
API views for the recipe app.
"""

from django.core.files.base import ContentFile
from django.db import transaction
from ninja import File, Query, Router
from ninja.files import UploadedFile
from typing import List

from app.utils_api import get_instance_detail
from ingredient.api_utils import get_or_create_ingredient
from ingredient.models import RecipeIngredient
from recipe.models import Recipe, Tag
from recipe.schemas import (
    RecipeFilter,
    RecipeIn,
    RecipeListSchema,
    RecipeOut,
    RecipePatch,
    TagListSchema
)
from recipe.utils import get_recipes_by_ings
from django.http import HttpResponse

tag_router = Router()
recipe_router = Router()


def set_recipe_ingredients(recipe, recipe_ings):
    """
    Override ingredients field with the ingredients passed.
    RecipeIngredient instances are created or deleted accordingly.
    """
    RecipeIngredient.objects.filter(recipe=recipe).delete()
    for recipe_ing_data in recipe_ings:
        name = recipe_ing_data.pop('name')
        display_unit = recipe_ing_data.pop('unit')
        ingredient = get_or_create_ingredient(name, recipe.user)

        RecipeIngredient.create_with_display_unit(
            recipe=recipe,
            ingredient=ingredient,
            display_unit=display_unit,
            **recipe_ing_data
        )


def set_recipe_tags(recipe, tags: List[str]):
    """
    Override tags field with the tags passed.
    If a tag does not exist it is created.
    """
    recipe.tags.clear()
    for tag_name in tags:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        if created:
            tag.added_by = recipe.user
        recipe.tags.add(tag)
    recipe.save()


@tag_router.get('/', response=List[TagListSchema],
                url_name='tags')
def tag_list(request):
    """Retrieve all tags in the system."""
    queryset = Tag.objects.all().order_by('name')
    return queryset


@recipe_router.get('/', response=List[RecipeListSchema],
                   url_name='recipes')
def recipe_list(
        request, ingredients: str | None = None,
        filters: RecipeFilter = Query(...)):
    """Retrieve all user's recipes."""
    user = request.auth
    queryset = Recipe.objects.filter(user=user).order_by('title')
    if ingredients:
        ing_list = ingredients.split(',')
        queryset = get_recipes_by_ings(queryset, ing_list)
    queryset = filters.filter(queryset)
    return queryset


@recipe_router.post('/', response={201: RecipeOut})
@transaction.atomic
def create_recipe(request, payload: RecipeIn):
    """Create a new recipe."""
    user = request.auth
    payload_dict = payload.dict()
    tags = payload_dict.pop('tags')
    recipe_ings = payload_dict.pop('ingredients')
    recipe = Recipe.objects.create(user=user, **payload_dict)
    set_recipe_tags(recipe, tags)
    recipe.refresh_from_db()
    set_recipe_ingredients(recipe, recipe_ings)

    return 201, recipe


@recipe_router.get('/{recipe_id}', response=RecipeOut,
                   url_name='recipe_detail')
def recipe_detail(request, recipe_id: int):
    """Retrieve details of a recipe."""
    recipe = get_instance_detail(recipe_id, Recipe, request.auth)
    return recipe


@recipe_router.patch('/{recipe_id}', response=RecipeOut)
@transaction.atomic
def recipe_update(request, recipe_id: int, payload: RecipePatch):
    """Update a recipe."""
    recipe = get_instance_detail(recipe_id, Recipe, request.auth)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr == 'tags':
            set_recipe_tags(recipe, tags=value)
            recipe.refresh_from_db()
        elif attr == 'ingredients':
            set_recipe_ingredients(recipe, recipe_ings=value)
        else:
            setattr(recipe, attr, value)
    recipe.save()
    return recipe


@recipe_router.delete('/{recipe_id}', response={204: None})
def delete_recipe(request, recipe_id: int):
    """Delete a recipe."""
    recipe = get_instance_detail(recipe_id, Recipe, request.auth)
    recipe.delete()
    return 204, None


@recipe_router.get('/{recipe_id}/image', url_name='download_recipe_image')
def download_recipe_image(request, recipe_id: int):
    """Download the image of a recipe."""
    recipe = get_instance_detail(recipe_id, Recipe, request.auth)
    if recipe.image:
        image_data = open(recipe.image.path, 'rb').read()
        response = HttpResponse(image_data, content_type='image/jpeg')
        response['Content-Disposition'] = 'filename="recipe_image.jpg"'
        return response
    else:
        return HttpResponse('Image not found', status=404)


@recipe_router.post('/{recipe_id}/image', url_name='recipe_image')
def upload_recipe_image(
        request, recipe_id: int, img: UploadedFile = File(...)):
    """Upload an image to a recipe."""
    recipe = get_instance_detail(recipe_id, Recipe, request.auth)

    image_data = ContentFile(img.read())
    recipe.image.save(img.name, image_data)
    recipe.save()

    return {'success': True}


@recipe_router.delete('/{recipe_id}/image', response={204: None})
def delete_image(request, recipe_id: int):
    """Delete a recipe image."""
    recipe = get_instance_detail(recipe_id, Recipe, request.auth)
    recipe.image.delete()
    return 204, None
