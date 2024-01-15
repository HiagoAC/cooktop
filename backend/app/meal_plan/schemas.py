"""
Schemas for the apis in meal_plan app.
"""

from ninja import ModelSchema, Schema
from typing import Dict, List

from meal_plan.models import MealPlan
from recipe.schemas import RecipeOut


class MealPlanListSchema(ModelSchema):
    """Output schema for meal plan list."""

    class Meta:
        model = MealPlan
        fields = ['id', 'creation_date']


class MealPlanIn(Schema):
    """Input schema for meal plan."""
    requested_ingredients: List[str]
    cookings: int | None = None
    servings_per_meal: int | None = None


class MealSchema(Schema):
    """Schema for meals in meal plan."""
    main_dish: RecipeOut
    side_dish: RecipeOut
    salad: RecipeOut

    @staticmethod
    def resolve_main_dish(obj):
        return RecipeOut.from_orm(obj.main_dish)

    @staticmethod
    def resolve_side_dish(obj):
        return RecipeOut.from_orm(obj.side_dish)

    @staticmethod
    def resolve_salad(obj):
        return RecipeOut.from_orm(obj.salad)


class MealPlanOut(ModelSchema):
    """Output schema for meal plan detail."""
    meals: Dict[int, MealSchema]

    class Config:
        model = MealPlan
        model_exclude = ['user', 'meals']

    @staticmethod
    def resolve_meals(obj):
        meals = dict()
        for meal in obj.meals.all().order_by('day'):
            meals[meal.day] = MealSchema.from_orm(meal)
        return meals
