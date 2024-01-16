"""
API views for the meal_plan app.
"""

from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError
from typing import List

from meal_plan.meal_planner import MealPlanner
from meal_plan.models import Preferences, MealPlan
from meal_plan.schemas import (
    MealPlanListSchema,
    MealPlanIn,
    MealPlanOut,
    MealPlanPatch
)
from recipe.api import get_recipe_detail

meal_plan_router = Router()


def get_meal_plan_detail(meal_plan_id: int, user):
    """Return meal plan if it belongs to user."""
    meal_plan = get_object_or_404(MealPlan, id=meal_plan_id)
    if meal_plan.user != user:
        raise HttpError(401, "Unauthorized")
    return meal_plan


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
    meal_plan = get_meal_plan_detail(meal_plan_id, request.auth)
    return meal_plan


@meal_plan_router.patch('/{meal_plan_id}', response=MealPlanOut)
@transaction.atomic
def meal_plan_update(request, meal_plan_id: int, payload: MealPlanPatch):
    """Update recipes in a meal plan."""
    user = request.auth
    meal_plan = get_meal_plan_detail(meal_plan_id, user)
    for day, meal in payload.dict()['meals'].items():
        for recipe_type, recipe_id in meal.items():
            if meal_plan.meals.filter(day=day).exists():
                meal_in_plan = meal_plan.meals.filter(day=day).first()
                setattr(
                    meal_in_plan,
                    recipe_type,
                    get_recipe_detail(recipe_id, user)
                )
                meal_in_plan.save()
    meal_plan.refresh_from_db()
    return meal_plan
