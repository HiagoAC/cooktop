# Generated by Django 4.2.8 on 2023-12-16 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredient', '0002_alter_ingredient_added_by_ingredientinpantry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientinpantry',
            name='measurement_unit',
            field=models.CharField(choices=[('g', 'gram'), ('ml', 'milliliter'), ('un', 'unit')], default='un', max_length=3),
        ),
    ]
