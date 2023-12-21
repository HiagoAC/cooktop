"""
API views for the recipe app.
"""

from ninja import Router
from typing import List

from recipe.models import Recipe, Tag
from recipe.schemas import RecipeListSchema, TagListSchema

tag_router = Router()
recipe_router = Router()


@tag_router.get('/', response=List[TagListSchema],
                url_name='tag_list')
def tag_list(request):
    """Retrieve all tags in the system."""
    queryset = Tag.objects.all().order_by('name')
    return queryset


@recipe_router.get('/', response=List[RecipeListSchema],
                   url_name='recipe_list')
def recipe_list(request):
    """Retrieve all user's recipes."""
    user = request.auth
    queryset = Recipe.objects.filter(user=user).order_by('title')
    return queryset
