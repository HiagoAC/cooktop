"""
API views for the meal_plan app.
"""

from ninja import Router
from typing import List

from meal_plan.models import MealPlan
from meal_plan.schemas import MealPlanListSchema

meal_plan_router = Router()


@meal_plan_router.get('/', response=List[MealPlanListSchema],
                      url_name='meal_plans')
def meal_plan_list(request):
    """Retrieve all meal plans in the system."""
    queryset = MealPlan.objects.all().order_by('-creation_date')
    return queryset
