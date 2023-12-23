"""
Schemas for the apis in ingredient app.
"""

from ninja import ModelSchema, Schema
from typing import List

from recipe.models import Recipe
from ingredient.models import RecipeIngredient


class TagListSchema(Schema):
    """Output schema for tag list."""
    id: int
    name: str


class RecipeListSchema(Schema):
    """Output schema for recipe list."""
    id: int
    title: str


class RecipeIngredientIn(ModelSchema):
    class Config:
        model = RecipeIngredient
        model_exclude = ['id', 'recipe', 'ingredient']


class RecipeIn(ModelSchema):
    """Input schema for recipe detail."""
    tags: List[str] = []
    ingredients: List[RecipeIngredientIn] = []

    class Config:
        model = Recipe
        model_exclude = ['id', 'user', 'image']
        fields_optional = ['description', 'time_minutes', 'notes']


class RecipeOut(ModelSchema):
    """Output schema for recipe detail."""
    tags: List[str]

    class Config:
        model = Recipe
        model_exclude = ['user', 'tags',]

    @staticmethod
    def resolve_tags(obj):
        tag_names = []
        for tag in obj.tags.all():
            tag_names.append(tag.name)
        return tag_names
