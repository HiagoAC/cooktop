"""
API views for the recipe app.
"""


from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError
from typing import List

from ingredient.api_utils import get_or_create_ingredient
from ingredient.models import RecipeIngredient
from recipe.models import Recipe, Tag
from recipe.schemas import RecipeListSchema, RecipeIn, RecipeOut, TagListSchema

tag_router = Router()
recipe_router = Router()


def get_recipe_detail(recipe_id: int, user):
    """
    Return recipe if it belongs to user.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.user != user:
        raise HttpError(401, "Unauthorized")
    return recipe


@tag_router.get('/', response=List[TagListSchema],
                url_name='tags')
def tag_list(request):
    """Retrieve all tags in the system."""
    queryset = Tag.objects.all().order_by('name')
    return queryset


@recipe_router.get('/', response=List[RecipeListSchema],
                   url_name='recipes')
def recipe_list(request):
    """Retrieve all user's recipes."""
    user = request.auth
    queryset = Recipe.objects.filter(user=user).order_by('title')
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
    for tag_name in tags:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        if created:
            tag.added_by = user
        recipe.tags.add(tag)
    recipe.save()
    for recipe_ing_data in recipe_ings:
        name = recipe_ing_data.pop('name')
        ingredient = get_or_create_ingredient(name, user)

        RecipeIngredient.create_with_display_unit(
            recipe=recipe,
            ingredient=ingredient,
            **recipe_ing_data
        )

    return 201, recipe


@recipe_router.get('/{recipe_id}', response=RecipeOut,
                   url_name='recipe_detail')
def pantry_detail(request, recipe_id: int):
    """Retrieve details of an ingriendt in pantry."""
    recipe = get_recipe_detail(recipe_id, request.auth)
    return recipe
