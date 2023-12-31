"""
Tests for the measurement_units module.
"""

from django.test import TestCase

from ingredient.measurement_units import DisplayUnit


class DisplayUnitTests(TestCase):
    """Tests for the DisplayUnit class."""

    def test_convert_unit(self):
        """Test that conversion is done correctly."""
        kg = DisplayUnit('kg', 'weight', 1000)
        quantity_grams = kg.convert_quantity(2)

        self.assertEqual(quantity_grams, 2000)

    def test_wrong_type(self):
        """Test entering an invalid type raises ValueError."""
        with self.assertRaises(ValueError):
            DisplayUnit('pascal', 'density', 1000)
