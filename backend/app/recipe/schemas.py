"""
Schemas for the apis in ingredient app.
"""

from django.db.models import Q
from ninja import (
    FilterSchema,
    ModelSchema,
    Schema
)
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


class RecipeIngredientSchema(ModelSchema):
    name: str

    class Config:
        model = RecipeIngredient
        model_exclude = ['id', 'recipe', 'ingredient', 'measurement_unit']


class RecipeIn(ModelSchema):
    """Input schema for recipe detail."""
    ingredients: List[RecipeIngredientSchema] = []
    tags: List[str] = []

    class Config:
        model = Recipe
        model_exclude = ['id', 'user', 'image']
        fields_optional = ['description', 'time_minutes', 'notes']


class RecipeOut(ModelSchema):
    """Output schema for recipe detail."""
    ingredients: List[RecipeIngredientSchema]
    tags: List[str]

    class Config:
        model = Recipe
        model_exclude = ['user', 'tags']

    @staticmethod
    def resolve_tags(obj):
        tag_names = []
        for tag in obj.tags.all():
            tag_names.append(tag.name)
        return tag_names

    @staticmethod
    def resolve_ingredients(obj):
        ings_data = []
        for recipe_ing in RecipeIngredient.objects.filter(recipe=obj):
            ings_data.append({
                'name': recipe_ing.ingredient.name,
                'quantity': recipe_ing.get_display_quantity(),
                'display_unit': recipe_ing.display_unit
            })
        return ings_data


class RecipePatch(ModelSchema):
    """Input schema for recipe patch."""
    ingredients: List[RecipeIngredientSchema] = []
    tags: List[str] = []
    title: str = ''
    directions: List[str] = []
    descriptions: str = ''

    class Config:
        model = Recipe
        model_exclude = ['id', 'user', 'image']
        fields_optional = '__all__'


class RecipeFilter(FilterSchema):
    """Schema for recipe filters."""
    tags: str | None = None

    def filter_tags(self, value: str) -> Q:
        if not value:
            return Q()
        tags = value.split(',')
        return Q(tags__name__in=tags)
