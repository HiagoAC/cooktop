"""
Record of display units for ingredients in recipes.
"""

from ingredient.models import MeasurementUnits


class DisplayUnit:
    """
    Display unit for ingredient in recipe.
    unit_type must be volume, weight, or unit
    """
    def __init__(self, unit: str, unit_type: str, conversion_rate: float):
        if unit_type not in ('volume', 'weight', 'unit'):
            raise ValueError('unit type is invalid.')
        self.unit = unit
        self.unit_type = unit_type
        self.conversion_rate = conversion_rate

    def convert_unit(self, quantity):
        return quantity * self.conversion_rate

    def get_standard_unit(self):
        if self.unit_type == 'volume':
            return MeasurementUnits.MILLILITER
        if self.unit_type == 'weight':
            return MeasurementUnits.GRAM
        else:
            return MeasurementUnits.UNIT


DISPLAY_UNITS = {
    'teaspoon': DisplayUnit('teaspoon', 'volume', 4.93),
    'tablespoon': DisplayUnit('tablespoon', 'volume', 14.79),
    'cup': DisplayUnit('cup', 'volume', 236.59),
    'gram': DisplayUnit('gram', 'weight', 1),
    'ml': DisplayUnit('ml', 'weight', 1),
    'unit': DisplayUnit('unit', 'unit', 1)
}
