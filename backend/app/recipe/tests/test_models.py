"""
Tests for Recipe app models.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from ingredient.models import Ingredient
from recipe.models import Recipe, RecipeIngredient, Tag


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

    def delete_recipe_unused_tags(self):
        """Test that deleting a recipe deletes unused tags as well."""
        unused = 'unused tag'
        used = 'used tag'
        tag_1 = Tag.objects.create(name=unused)
        tag_2 = Tag.objects.create(name=used)
        user = create_user()
        title = 'a recipe'
        recipe = Recipe.objects.create(
            user=user,
            title=title,
            directions=['a step'],
            tags=[tag_1, tag_2]
        )
        Recipe.objects.create(
            user=create_user(email='another_email@example.com'),
            title='another recipe',
            directions=['a step'],
            tags=[tag_2]
        )

        recipe.delete()

        self.assertFalse(Recipe.objects.filter(
            user=user, title=title).exists())
        self.assertFalse(Tag.objects.filter(name=unused))
        self.assertTrue(Tag.objects.filter(name=used))


class RecipeIngredientModelTests(TestCase):
    """Tests for the RecipeIngredient model."""

    def test_add_ingredient_to_recipe(self):
        """Test creating RecipeIngredient instance."""
        recipe = Recipe.objects.create(
            user=create_user(),
            title='title',
            directions=['step 1']
        )
        ing = Ingredient.objects.create(name='ing')
        recipe_ing = RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=ing,
            quantity=473.18,
            measurement_unit='ml',
            display_unit='cup'
        )
        self.assertEqual(str(recipe_ing), f'{str(ing)} in {str(recipe)}')


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
