"""
Schemas for the apis in ingredient app.
"""

from ninja import Schema


class TagListSchema(Schema):
    """Output schema for tag_list."""
    id: int
    name: str


class RecipeListSchema(Schema):
    """Output schema for tag_list."""
    id: int
    title: str
