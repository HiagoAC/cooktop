"""Utility functions for the Recipe app."""

from django.db.models import Count, Q, QuerySet
from typing import List

from recipe.models import Recipe


def annotate_by_ing_count(
        queryset: QuerySet[Recipe], ingredients: List[str]) -> QuerySet:
    """annotate the number of matches in recipes of the given queryset."""
    query_expression = Q(
        recipeingredient__ingredient__name__in=ingredients)
    return queryset.annotate(
        match_count=Count(
            'recipeingredient', filter=query_expression)
            )


def get_recipes_by_ings(
        queryset: QuerySet[Recipe], ingredients: List[str]) -> QuerySet:
    """
    Order recipes in the queryset by the number of ingredients in the
    given list of ingredients the recipe contains.
    Recipes that contain 0 of the given ingredients are filtered out.
    """
    queryset = annotate_by_ing_count(queryset, ingredients)
    # filter out 0 matches recipes and order by match count
    queryset = queryset.filter(match_count__gt=0).order_by('-match_count')

    return queryset
