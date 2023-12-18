"""
Utitility functions for tests.
"""

import jwt

from datetime import timedelta
from django.contrib.auth import get_user_model
from time import time

from user.auth_handler import JWT_SECRET, JWT_ALGO


def create_user(email='example@test.com'):
    """Create a user."""
    return get_user_model().objects.create_user(
        email=email, password='password321')


def auth_header(user):
    """Return a header with a valid token for the given user."""
    token_data = {
        'email': user.email,
        'exp': time() + timedelta(minutes=10).total_seconds(),
        'sub': 'access_token',
    }
    access_token = jwt.encode(token_data, JWT_SECRET, algorithm=JWT_ALGO)
    headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
    return headers
