# Generated by Django 4.2.8 on 2024-01-05 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meal_plan', '0005_delete_mealplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='MealPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('meals', models.ManyToManyField(to='meal_plan.meal')),
            ],
        ),
    ]