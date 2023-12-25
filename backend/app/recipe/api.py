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
from recipe.schemas import (
    RecipeListSchema,
    RecipeIn,
    RecipeOut,
    RecipePatch,
    TagListSchema
)

tag_router = Router()
recipe_router = Router()


def get_recipe_detail(recipe_id: int, user):
    """Return recipe if it belongs to user."""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.user != user:
        raise HttpError(401, "Unauthorized")
    return recipe


def set_recipe_ingredients(recipe, recipe_ings):
    """
    Override ingredients field with the ingredients passed.
    RecipeIngredient instances are created or deleted accordingly.
    """
    RecipeIngredient.objects.filter(recipe=recipe).delete()
    for recipe_ing_data in recipe_ings:
        name = recipe_ing_data.pop('name')
        ingredient = get_or_create_ingredient(name, recipe.user)

        RecipeIngredient.create_with_display_unit(
            recipe=recipe,
            ingredient=ingredient,
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
    set_recipe_tags(recipe, tags)
    recipe.refresh_from_db()
    set_recipe_ingredients(recipe, recipe_ings)

    return 201, recipe


@recipe_router.get('/{recipe_id}', response=RecipeOut,
                   url_name='recipe_detail')
def recipe_detail(request, recipe_id: int):
    """Retrieve details of a recipe."""
    recipe = get_recipe_detail(recipe_id, request.auth)
    return recipe


@recipe_router.patch('/{recipe_id}', response=RecipeOut)
@transaction.atomic
def recipe_update(request, recipe_id: int, payload: RecipePatch):
    """Update a recipe."""
    recipe = get_recipe_detail(recipe_id, request.auth)
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
