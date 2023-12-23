"""
API views for the recipe app.
"""

from ninja import Router
from typing import List

from recipe.models import Recipe, Tag
from recipe.schemas import RecipeListSchema, RecipeIn, RecipeOut, TagListSchema

tag_router = Router()
recipe_router = Router()


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
def create_recipe(request, payload: RecipeIn):
    """Create a new recipe."""
    user = request.auth
    payload_dict = payload.dict()
    tags = payload_dict.pop('tags')
    payload_dict.pop('ingredients')
    recipe = Recipe.objects.create(user=user, **payload_dict)
    for tag_name in tags:
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        recipe.tags.add(tag)
    recipe.save()
    return 201, recipe
