# Generated by Django 4.2.9 on 2024-01-28 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredient', '0009_shoppinglistitem_display_unit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='shoppinglistitem',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
    ]
