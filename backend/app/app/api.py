"""
API views.
"""
from ninja import NinjaAPI
from user.api import router as user_router

api = NinjaAPI(urls_namespace='api')

api.add_router('users/', user_router)
