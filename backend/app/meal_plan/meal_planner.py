"""Meal Planner module."""

from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils import timezone
from random import choice
from typing import Dict, List

from ingredient.models import Ingredient, RecipeIngredient
from meal_plan.models import Meal, MealPlan
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
        Pick recipe in the given of the queryset. Indices out of queryset
        range are accessed circularly. Ex: len(queryset) = 1,
        len(queryset) + 1 = 2, ...
        """
        qs_index = index % len(queryset)
        return queryset[qs_index]

    def _make_meals(
            self,
            querysets: Dict[str, QuerySet[Recipe]],
            number_meals: int,
            ) -> List[Meal]:
        """
        Make a specified number of meals based on a filtered queryset of
        recipes.
        """
        meals = list()
        for i in range(number_meals):
            meal = Meal.objects.create(day=i+1)
            for recipe_type, queryset in querysets.items():
                if not queryset.exists():
                    dish = self._pick_random_recipe(
                        self.user_recipes[recipe_type])
                else:
                    dish = self._pick_recipe_by_index(queryset, i)
                setattr(meal, recipe_type, dish)
            meal.save()
            meals.append(meal)

        return meals

    def generate_plan(
            self,
            requested_ingredients: List[str] | None = None,
            cookings: int = 7,
            servings_per_meal: int = 2
            ) -> MealPlan:
        """
        Generate a meal plan based on the ingredients in user's pantry
        ingredients passed. This meal plan favors recipes with overlapping
        ingredients.
        """
        # Validation
        if not 0 < cookings <= 7:
            raise ValueError("Cookings must be between 1 and 7.")
        if servings_per_meal <= 0:
            raise ValueError("Servings per meal must be greater than 0.")

        # Get base meals with required ingredients and pantry ingredients.
        filtered_recipes = self._filter_user_recipes_by_ingredients(
            requested_ingredients)
        filtered_recipes = self._reorder_by_expiring_ings(filtered_recipes)
        base_meals = self._make_meals(
            querysets=filtered_recipes, number_meals=min(2, cookings))

        # Get list of ingredients in base meals
        base_ings = list()
        for meal in base_meals:
            for recipe in (meal.main_dish, meal.side_dish, meal.salad):
                base_ings.extend(
                    RecipeIngredient.objects
                    .filter(recipe=recipe)
                    .values_list('ingredient__name', flat=True)
                    )

        # Get meals with overlapping ingredients with base meals.
        querysets = self.user_recipes
        for key in querysets:
            querysets[key] = get_recipes_by_ings(querysets[key], base_ings)
        other_meals = self._make_meals(
            querysets=querysets,
            number_meals=cookings - len(base_meals)
            )

        # Adjust day in other_meals.
        day = len(base_meals)
        for meal in other_meals:
            meal.day = day
            day += 1

        # Create meal_plan
        meal_plan = MealPlan.objects.create(
            user=self.user, servings_per_meal=servings_per_meal)
        meal_plan.meals.add(*base_meals)
        meal_plan.meals.add(*other_meals)

        return meal_plan
