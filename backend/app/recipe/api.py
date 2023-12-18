"""
API views for the recipe app.
"""

from ninja import Router
from typing import List

from recipe.models import Tag
from recipe.schemas import TagListSchema

tag_router = Router()


@tag_router.get('/', response=List[TagListSchema],
                url_name='tag_list')
def tag_list(request):
    """Retrieve all tags in the system."""
    queryset = Tag.objects.all().order_by('name')
    return queryset
