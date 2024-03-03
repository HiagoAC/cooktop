"""
API views.
"""
from ninja import NinjaAPI
from ninja.errors import ValidationError

from user.auth_handler import AuthHandler, InvalidAccessTokenError
from user.api import user_router, token_router
from ingredient.api import pantry_router, shopping_list_router
from meal_plan.api import meal_plan_router, preferences_router
from recipe.api import tag_router, recipe_router

api = NinjaAPI(urls_namespace='api', auth=AuthHandler())


api.add_router('meal-plans/', meal_plan_router)
api.add_router('pantry/', pantry_router)
api.add_router('preferences/', preferences_router)
api.add_router('recipes/', recipe_router)
api.add_router('shopping_list/', shopping_list_router)
api.add_router('tags/', tag_router)
api.add_router('tokens/', token_router)
api.add_router('users/', user_router)


@api.exception_handler(InvalidAccessTokenError)
def on_invalid_token(request, exc):
    return api.create_response(
        request, {"detail": "Invalid token supplied."}, status=401)


@api.exception_handler(ValidationError)
def on_validation_error(request, exc):
    print(exc.errors)
    return api.create_response(request, {'detail': exc.errors}, status=422)
