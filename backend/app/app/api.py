"""
API views.
"""
from ninja import NinjaAPI

from user.auth_handler import AuthHandler
from user.api import user_router, token_router

api = NinjaAPI(urls_namespace='api', auth=AuthHandler())

api.add_router('users/', user_router)
api.add_router('token/', token_router)
