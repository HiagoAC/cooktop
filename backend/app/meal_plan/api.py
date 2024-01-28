"""
API views for the meal_plan app.
"""

from django.db import transaction
from ninja import Router
from ninja.errors import HttpError
from typing import List

from app.utils_api import get_instance_detail
from meal_plan.meal_planner import MealPlanner
from meal_plan.models import Preferences, Meal, MealPlan
from meal_plan.schemas import (
    MealPlanListSchema,
    MealPlanIn,
    MealPlanOut,
    MealPlanPatch
)
from recipe.models import Recipe

meal_plan_router = Router()


@meal_plan_router.get('/', response=List[MealPlanListSchema],
                      url_name='meal_plans')
def meal_plan_list(request):
    """Retrieve all meal plans in the system."""
    user = request.auth
    queryset = MealPlan.objects.filter(user=user).order_by('-creation_date')
    return queryset


@meal_plan_router.post('/', response={201: MealPlanOut})
@transaction.atomic
def create_recipe(request, payload: MealPlanIn):
    """Create a new meal plan."""
    user = request.auth
    meal_planner = MealPlanner(user=user)
    data = payload.dict(exclude_unset=True)
    if (('cookings' not in data or 'servings_per_meal' not in data) and
            Preferences.objects.filter(user=user).exists()):
        preferences = Preferences.objects.get(user=user)
        if 'cookings' not in data:
            data['cookings'] = preferences.cookings_per_week
        if 'servings_per_meal' not in data:
            data['servings_per_meal'] = preferences.servings_per_meal

    meal_plan = meal_planner.generate_plan(**data)
    return meal_plan


@meal_plan_router.get('/{meal_plan_id}', response=MealPlanOut,
                      url_name='meal_plan_detail')
def meal_plan_detail(request, meal_plan_id: int):
    """Retrieve details of a meal plan."""
    meal_plan = get_instance_detail(meal_plan_id, MealPlan, request.auth)
    return meal_plan


@meal_plan_router.patch('/{meal_plan_id}', response=MealPlanOut)
@transaction.atomic
def meal_plan_update(request, meal_plan_id: int, payload: MealPlanPatch):
    """Update recipes in a meal plan."""
    user = request.auth
    recipe_types = {
        'main_dish': Recipe.RecipeTypes.MAIN_DISH,
        'side_dish': Recipe.RecipeTypes.SIDE_DISH,
        'salad': Recipe.RecipeTypes.SALAD
    }
    meal_plan = get_instance_detail(meal_plan_id, MealPlan, request.auth)
    for day, meal in payload.dict()['meals'].items():
        for recipe_type, recipe_id in meal.items():
            if Meal.objects.filter(meal_plan=meal_plan, day=day).exists():
                meal_in_plan = Meal.objects.filter(day=day).first()
                recipe = get_instance_detail(recipe_id, Recipe, user)
                if recipe.recipe_type != recipe_types[recipe_type]:
                    raise HttpError(422, "Wrong recipe type.")
                setattr(
                    meal_in_plan,
                    recipe_type,
                    recipe
                )
                meal_in_plan.save()
    meal_plan.refresh_from_db()
    return meal_plan


@meal_plan_router.delete('/{meal_plan_id}', response={204: None})
def delete_meal_plan(request, meal_plan_id: int):
    """Delete a meal plan."""
    meal_plan = get_instance_detail(meal_plan_id, MealPlan, request.auth)
    meal_plan.delete()
    return 204, None


@meal_plan_router.post('/{meal_plan_id}/subtract-from-pantry',
                       response={204: None}, url_name='meal_plan_subtract')
@transaction.atomic
def subtract_ingredients_from_pantry(request, meal_plan_id: int):
    """
    Subtract ingredients of all meals in meal plan from pantry if they have
    not been subtracted yet.
    """
    meal_plan = get_instance_detail(meal_plan_id, MealPlan, request.auth)
    meal_plan.subtract_from_pantry()
    return 204, None
