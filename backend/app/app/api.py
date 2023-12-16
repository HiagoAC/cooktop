"""
API views.
"""
from ninja import NinjaAPI

from user.auth_handler import AuthHandler, InvalidAccessTokenError
from user.api import user_router, token_router
from ingredient.api import pantry_router

api = NinjaAPI(urls_namespace='api', auth=AuthHandler())

api.add_router('users/', user_router)
api.add_router('tokens/', token_router)
api.add_router('pantry/', pantry_router)


@api.exception_handler(InvalidAccessTokenError)
def on_invalid_token(request, exc):
    return api.create_response(
        request, {"detail": "Invalid token supplied."}, status=401)
