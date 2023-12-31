"""
Recipe app models.
"""

import os
import uuid

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models

User = get_user_model()


def recipe_image_file_path(instance, filename):
    """Generates a file path with a unique file name."""
    path = 'uploads/recipe/'
    ext = filename.split('.')[-1]
    new_name = f'{uuid.uuid4()}.{ext}'
    return os.path.join(path, new_name)


class Recipe(models.Model):
    """Recipe of a user."""
    # required
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    directions = ArrayField(models.TextField(max_length=1023))

    # optional
    description = models.TextField(blank=True, default='')
    servings = models.PositiveSmallIntegerField(default=1)
    time_minutes = models.PositiveSmallIntegerField(null=True, default=None)
    notes = models.TextField(blank=True, default='')
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(
        null=True, default=None, upload_to=recipe_image_file_path)

    def delete(self):
        """
        Delete recipe and tags that are not associated with other recipes.
        """
        tags = self.tags.all()
        for tag in tags:
            if not Recipe.objects.filter(tags=tag).exists():
                tag.delete()
        self.image.delete(save=False)
        super().delete()

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=63, unique=True)
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        default=None
    )

    def __str__(self):
        return self.name
