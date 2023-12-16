"""
Schemas for the apis in ingredient app.
"""
from datetime import date
from ninja import Schema


class PantryListSchema(Schema):
    """Output schema for pantry_list."""
    id: int
    name: str


class PantryDetailSchema(Schema):
    """Output schema for pantry_detail."""
    name: str
    quantity: float
    measurement_unit: str
    expiration: date | None
