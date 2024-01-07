# Generated by Django 4.2.8 on 2024-01-07 03:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meal_plan', '0008_delete_mealplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='MealPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servings_per_meal', models.PositiveSmallIntegerField(default=2)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('meals', models.ManyToManyField(to='meal_plan.meal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
