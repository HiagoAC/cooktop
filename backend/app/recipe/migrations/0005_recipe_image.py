# Generated by Django 4.2.8 on 2023-12-21 12:54

from django.db import migrations, models
import recipe.models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_delete_recipeingredient'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to=recipe.models.recipe_image_file_path),
        ),
    ]
