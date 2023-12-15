"""
Ingredient app models.
"""
from django.contrib.auth import get_user_model
from django.db import models


MEASUREMENT_UNITS = [
        ('g', 'Gram'),
        ('ml', 'Milliliter'),
        ('un', 'Unit')
    ]
User = get_user_model()


class Ingredient(models.Model):
    """Ingredient in the system."""
    name = models.CharField(max_length=63, unique=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
