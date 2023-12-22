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
