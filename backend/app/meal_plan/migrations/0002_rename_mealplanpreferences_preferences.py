# Generated by Django 4.2.8 on 2024-01-03 09:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meal_plan', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MealPlanPreferences',
            new_name='Preferences',
        ),
    ]
