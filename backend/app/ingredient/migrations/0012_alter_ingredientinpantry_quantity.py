# Generated by Django 4.2.11 on 2024-07-15 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredient', '0011_alter_ingredientinpantry_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientinpantry',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=6, null=True),
        ),
    ]
