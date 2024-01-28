"""
Schemas for the apis in ingredient app.
"""
from datetime import date
from ninja import ModelSchema, Schema
from pydantic import NonNegativeFloat

from ingredient.models import ShoppingListItem


class PantryListSchema(Schema):
    """Output schema for pantry_list."""
    id: int
    name: str


class PantryDetailIn(Schema):
    """Input schema for pantry_detail."""
    name: str
    quantity: NonNegativeFloat
    measurement_unit: str
    expiration: date | None = None


class PantryDetailPatch(Schema):
    """Input schema for pantry_detail patch."""
    name: str | None = None
    quantity: NonNegativeFloat | None = None
    measurement_unit: str | None = None
    expiration: date | None = None


class PantryDetailOut(PantryDetailIn):
    """Output schema for pantry_detail."""
    id: int


class ShoppingListItemOut(ModelSchema):
    """Output schema for shopping_list endpoints."""
    name: str
    quantity: NonNegativeFloat
    unit: str

    class Meta:
        model = ShoppingListItem
        fields = ['id']

    @staticmethod
    def resolve_name(obj):
        return obj.ingredient.name

    @staticmethod
    def resolve_quantity(obj):
        return obj.get_display_quantity()

    @staticmethod
    def resolve_unit(obj):
        return obj.display_unit
