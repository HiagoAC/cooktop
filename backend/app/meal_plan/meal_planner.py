"""Meal Planner module."""

from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet # noqa
from django.utils import timezone
from random import choice
from typing import Dict, List

from ingredient.models import Ingredient, RecipeIngredient # noqa
from meal_plan.models import Meal, MealPlan # noqa
from recipe.models import Recipe
from recipe.utils import annotate_by_ing_count, get_recipes_by_ings

User = get_user_model()


class MealPlanner():
    """Class for generating meal plans."""

    def __init__(self, user: User):
        self.user = user
        self.pantry_ings = Ingredient.objects.filter(
            ingredientinpantry__user=self.user)
        self.user_recipes = {
            'main_dish':  Recipe.objects.filter(
                user=user, recipe_type=Recipe.RecipeTypes.MAIN_DISH),
            'side_dish': Recipe.objects.filter(
                user=user, recipe_type=Recipe.RecipeTypes.SIDE_DISH),
            'salad': Recipe.objects.filter(
                user=user, recipe_type=Recipe.RecipeTypes.SALAD)
            }

    def _filter_user_recipes_by_ingredients(
            self,
            requested_ingredients: List[str]
            ) -> Dict[str, QuerySet[Recipe]]:
        """
        Filter and order user recipes by the list of requested ingredients
        combined with user's pantry ingredients.
        """
        # Combine ingredients for filtering recipes
        ingredients = list(requested_ingredients)
        ingredients.extend(self.pantry_ings.values_list('name', flat=True))

        # filter recipes by ingredients
        filtered_recipes = dict()
        for queryset in self.user_recipes:
            filtered_recipes[queryset] = get_recipes_by_ings(
                self.user_recipes[queryset], ingredients)

        return filtered_recipes

    def _reorder_by_expiring_ings(
            self,
            recipes: Dict[str, QuerySet[Recipe]]
            ) -> Dict[str, QuerySet[Recipe]]:
        """
        Reorder recipes by the number of ingredients expiring in the next
        week.
        """
        week_later = timezone.now().date() + timedelta(weeks=1)
        expiring_ings = self.pantry_ings.filter(
            ingredientinpantry__expiration__lte=week_later)
        expiring_ings = expiring_ings.values_list('name', flat=True)
        for queryset in recipes:
            recipes[queryset] = annotate_by_ing_count(
                recipes[queryset], expiring_ings)
            recipes[queryset] = recipes[queryset].order_by('-match_count')

        return recipes

    def _pick_random_recipe(
            self, queryset: QuerySet[Recipe]) -> Recipe:
        """Pick a random recipe from a queryset."""
        random_id = choice(queryset.values_list('id', flat=True))
        return queryset.get(id=random_id)

    def _pick_recipe_by_index(
            self, queryset: QuerySet[Recipe], index: int) -> Recipe:
        """
        - Pick recipe in the given of the queryset. Indices out of queryset
        range are accessed circularly. Ex: len(queryset) = 1,
        len(queryset) + 1 = 2, ...
        """
        qs_index = index % len(queryset)
        return queryset[qs_index]
