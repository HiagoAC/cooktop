"""
Schemas for the apis in meal_plan app.
"""

from ninja import ModelSchema

from meal_plan.models import MealPlan


class MealPlanListSchema(ModelSchema):
    """Output schema for meal plan list."""

    class Meta:
        model = MealPlan
        fields = ['id', 'creation_date']
