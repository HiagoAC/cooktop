"""
Utitility functions for APIs.
"""

from django.contrib.auth import get_user_model
from django.db.models import Model
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError

User = get_user_model()


def get_instance_detail(id: int, model: Model, user: User):
    """Return instace if it exists and belongs to user."""
    recipe = get_object_or_404(model, id=id)
    if recipe.user != user:
        raise HttpError(401, "Unauthorized")
    return recipe
