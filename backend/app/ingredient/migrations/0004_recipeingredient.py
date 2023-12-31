# Generated by Django 4.2.8 on 2023-12-18 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_delete_recipeingredient'),
        ('ingredient', '0003_alter_ingredientinpantry_measurement_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('measurement_unit', models.CharField(choices=[('g', 'gram'), ('ml', 'milliliter'), ('un', 'unit')], default='un', max_length=3)),
                ('display_unit', models.CharField(max_length=20)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingredient.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.recipe')),
            ],
        ),
    ]
