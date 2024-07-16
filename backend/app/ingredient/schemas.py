"""
Schemas for the apis in ingredient app.
"""
from datetime import date
from ninja import Schema
from pydantic import NonNegativeFloat


class PantryDetailIn(Schema):
    """Input schema for pantry_detail."""
    name: str
    quantity: NonNegativeFloat
    unit: str
    expiration: date | None = None


class PantryDetailPatch(Schema):
    """Input schema for pantry_detail patch."""
    name: str | None = None
    quantity: NonNegativeFloat | None = None
    unit: str | None = None
    expiration: date | None = None


class PantryDetailOut(PantryDetailIn):
    """Output schema for pantry_detail."""
    id: int

    @staticmethod
    def resolve_name(obj):
        return obj.ingredient.name

    @staticmethod
    def resolve_quantity(obj):
        return obj.get_display_quantity()

    @staticmethod
    def resolve_unit(obj):
        return obj.display_unit


class ShoppingListItemIn(Schema):
    """Input schema for shopping_list endpoints."""
    name: str
    quantity: NonNegativeFloat
    unit: str


class ShoppingListItemOut(ShoppingListItemIn):
    """Output schema for shopping_list endpoints."""
    id: int

    @staticmethod
    def resolve_name(obj):
        return obj.ingredient.name

    @staticmethod
    def resolve_quantity(obj):
        return obj.get_display_quantity()

    @staticmethod
    def resolve_unit(obj):
        return obj.display_unit


class ShoppingListItemPatch(Schema):
    """Input schema for shopping_list_detail patch."""
    name: str | None = None
    quantity: NonNegativeFloat | None = None
    unit: str | None = None
