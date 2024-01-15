"""
API views for the meal_plan app.
"""

from django.db import transaction
from ninja import Router
from typing import List

from meal_plan.meal_planner import MealPlanner
from meal_plan.models import MealPlan
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
    meal_plan = meal_planner.generate_plan(**payload.dict(exclude_unset=True))
    return meal_plan
