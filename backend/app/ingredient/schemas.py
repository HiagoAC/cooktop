"""
Schemas for the apis in ingredient app.
"""
from datetime import date
from ninja import Schema
from pydantic import NonNegativeFloat


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


class PantryDetailOut(PantryDetailIn):
    """Output schema for pantry_detail."""
    id: int
