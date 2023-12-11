"""
API views.
"""
from ninja import NinjaAPI

from user.api import user_router, token_router

api = NinjaAPI(urls_namespace='api')

api.add_router('users/', user_router)
api.add_router('token/', token_router)
