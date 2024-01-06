# Generated by Django 4.2.8 on 2024-01-05 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_alter_recipe_description_alter_recipe_notes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='recipe_type',
            field=models.CharField(choices=[('mai', 'main dish'), ('sid', 'side dish'), ('sal', 'salad'), ('des', 'dessert'), ('sna', 'snack')], default='mai', max_length=3),
        ),
    ]