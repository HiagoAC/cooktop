"""
Tests for Recipe app models.
"""

import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from unittest.mock import patch

from app.utils_test import(
    create_recipe,
    create_recipe_ing,
    create_sample_image,
    create_user
)
from recipe.models import Recipe, Tag, recipe_image_file_path


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

    def test_ingredient_match_count(self):
        """Test that ingredient_match_count method works correctly."""
        recipe = create_recipe(user=create_user())
        create_recipe_ing(recipe, 'ing_1')
        create_recipe_ing(recipe, 'ing_2')
        another_recipe = create_recipe(
            user=create_user('another_user@example.com'), title='title')
        create_recipe_ing(another_recipe, 'ing_3')
        match_count = recipe.ingredient_match_count(
            ['ing_1', 'ing_2', 'ing_3'])
        self.assertEqual(match_count, 2)

    def test_delete_recipe_unused_tags(self):
        """Test that deleting a recipe deletes unused tags as well."""
        unused = 'unused tag'
        used = 'used tag'
        Tag.objects.create(name=unused)
        Tag.objects.create(name=used)
        user = create_user()
        title = 'a recipe'
        recipe = create_recipe(
            user=user,
            tags=[unused, used],
            title=title,
            directions=['a step'],
        )
        create_recipe(
            user=create_user(email='another_email@example.com'),
            tags=[used],
            title='another recipe',
            directions=['a step'],
        )

        recipe.delete()

        self.assertFalse(Recipe.objects.filter(
            user=user, title=title).exists())
        self.assertFalse(Tag.objects.filter(name=unused).exists())
        self.assertTrue(Tag.objects.filter(name=used).exists())


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


class RecipeImageTests(TestCase):
    """Tests for recipes' images."""

    def setUp(self):
        self.recipe = create_recipe(create_user())
        self.image = create_sample_image()
        self.recipe.image = SimpleUploadedFile(
            name='test.jpg',
            content=self.image.read(),
            content_type='image/jpeg'
        )
        self.recipe.save()
        self.image_path = self.recipe.image.path

    def tearDown(self):
        if os.path.exists(self.image_path):
            os.remove(self.image_path)

    @patch('recipe.models.uuid.uuid4')
    def test_recipe_image_file_path(self, mock_uuid):
        """Test that recipe image files are generated correctly."""
        uuid = 'test_uuid'
        mock_uuid.return_value = uuid
        file_path = recipe_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg')

    def test_image_deleted_with_recipe(self):
        """
        Test that an image associated with a recipe is deleted when the recipe
        is deleted.
        """
        self.recipe.delete()

        self.assertFalse(os.path.exists(self.image_path))
