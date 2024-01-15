"""
API views for the meal_plan app.
"""

from django.db import transaction
from ninja import Router
from typing import List

from meal_plan.meal_planner import MealPlanner
from meal_plan.models import Preferences, MealPlan
from meal_plan.schemas import MealPlanListSchema, MealPlanIn, MealPlanOut

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
