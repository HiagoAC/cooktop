"""
Recipe app models.
"""

import os
import uuid

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


def recipe_image_file_path(instance, filename):
    """Generates a file path with a unique file name."""
    path = 'uploads/recipe/'
    ext = filename.split('.')[-1]
    new_name = f'{uuid.uuid4()}.{ext}'
    return os.path.join(path, new_name)


class Recipe(models.Model):
    """Recipe of a user."""

    class RecipeTypes(models.TextChoices):
        MAIN_DISH = 'mai', _('main dish')
        SIDE_DISH = 'sid', _('side dish')
        SALAD = 'sal', _('salad')
        DESSERT = 'des', _('dessert')
        SNACK = 'sna', _('snack')

    # required
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=63)
    directions = ArrayField(models.TextField(max_length=1023))

    # optional
    description = models.TextField(max_length=300, blank=True, default='')
    servings = models.PositiveSmallIntegerField(default=1)
    time_minutes = models.PositiveSmallIntegerField(null=True, default=None)
    recipe_type = models.CharField(
        max_length=3,
        choices=RecipeTypes.choices,
        default=RecipeTypes.MAIN_DISH
    )
    notes = models.TextField(blank=True, default='')
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(
        null=True, default=None, upload_to=recipe_image_file_path)

    def delete(self):
        """
        Delete recipe and tags that are not associated with other recipes.
        """
        tags = list(self.tags.all())
        self.image.delete(save=False)
        super().delete()
        for tag in tags:
            if not Recipe.objects.filter(tags=tag).exists():
                tag.delete()

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
