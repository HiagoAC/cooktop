
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Preferences(models.Model):
    """General user's preferences for meal plans."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    servings_per_week = models.PositiveSmallIntegerField(default=1)
    cookings_per_week = models.PositiveSmallIntegerField(default=7)


class MealPlan(models.Model):
    """User's meal plan for the week."""
    pass
