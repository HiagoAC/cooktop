"""
Record of display units for ingredients in recipes.
"""

from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _


class MeasurementUnits(models.TextChoices):
    GRAM = 'g', _('gram')
    MILLILITER = 'ml', _('milliliter')
    UNIT = 'un', _('unit')


class DisplayUnit:
    """
    Display unit for ingredient in recipe.
    unit_type must be volume, weight, or unit
    """
    def __init__(self, unit: str, unit_type: str, conversion_rate: str):
        if unit_type not in ('volume', 'weight', 'unit'):
            raise ValueError('unit type is invalid.')
        self.unit = unit
        self.unit_type = unit_type
        self.conversion_rate = Decimal(conversion_rate)

    def convert_quantity(self, quantity):
        """
        Convert quantity from display unit to storage measurement unit.
        """
        result = Decimal(str(quantity)) * self.conversion_rate
        return result.quantize(Decimal('0.00'))

    def convert_to_display_unit(self, quantity):
        """
        Convert quantity from storage measurement unit to display unit.
        """
        result = Decimal(str(quantity)) / self.conversion_rate
        return result.quantize(Decimal('0.00'))

    def get_standard_unit(self):
        if self.unit_type == 'volume':
            return MeasurementUnits.MILLILITER
        if self.unit_type == 'weight':
            return MeasurementUnits.GRAM
        else:
            return MeasurementUnits.UNIT


DISPLAY_UNITS = {
    'teaspoon': DisplayUnit('teaspoon', 'volume', '4.93'),
    'tablespoon': DisplayUnit('tablespoon', 'volume', '14.79'),
    'cup': DisplayUnit('cup', 'volume', '236.59'),
    'gram': DisplayUnit('gram', 'weight', '1.00'),
    'ml': DisplayUnit('ml', 'weight', '1.00'),
    'unit': DisplayUnit('unit', 'unit', '1.00')
}
