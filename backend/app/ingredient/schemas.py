"""
Schemas for the apis in ingredient app.
"""
from ninja import Schema


class PantryListSchema(Schema):
    """Output schema for pantry_list"""
    id: int
    name: str
