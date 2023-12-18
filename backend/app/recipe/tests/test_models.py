"""
Tests for Recipe app models.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from recipe.models import Recipe, Tag


def create_user(email='example@test.com'):
    """Create a user."""
    return get_user_model().objects.create_user(
        email=email, password='password321')


class RecipeModelTests(TestCase):
    """Tests for the Recipe model."""

    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = create_user()
        directions = ['step 1', 'step 2']
        recipe = Recipe.objects.create(
            user=user,
            title='a recipe',
            directions=directions
        )

        self.assertEqual(str(recipe), recipe.title)
        self.assertEqual(len(recipe.directions), len(directions))


class TagModelTests(TestCase):
    """Tests for the Tag model."""

    def test_create_tag(self):
        """Test creating a tag."""
        name = 'a_tag'
        tag = Tag.objects.create(name=name)

        self.assertEqual(tag.name, name)
        self.assertEqual(str(tag), tag.name)

    def test_delete_user_that_added_tag(self):
        """
        Tests that deleting the user that created the tag sets
        ingredient's added_by field to None instead of deleting the
        tag.
        """
        user = create_user()
        tag = Tag.objects.create(name='a_tag', added_by=user)

        self.assertEqual(tag.added_by, user)

        user.delete()
        tag.refresh_from_db()

        self.assertIsNone(tag.added_by)