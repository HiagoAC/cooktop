"""
Recipe app models.
"""

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=63)
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        default=None
    )

    def __str__(self):
        return self.name
