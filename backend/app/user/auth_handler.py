"""
Authentication handling functionality.
"""
import jwt
import time

from django.contrib.auth import get_user_model
from datetime import timedelta
from decouple import AutoConfig
# from ninja.security import HttpBearer

from user.models import RefreshToken

config = AutoConfig()
JWT_SECRET = config('secret')
JWT_ALGO = config('algo')


class AuthHandler():  # class AuthHandler(HttpBearer):
    """Handle user authentication in the system."""

    def encode_tokens(self, email):
        """
        Generates a new pair of access and refresh tokens.
        """
        access_payload = {
            'email': email,
            'exp': time.time() + timedelta(minutes=10).total_seconds(),
            'sub': 'access_token',
        }
        refresh_payload = {
            'email': email,
            'exp': time.time() + timedelta(days=7).total_seconds(),
            'sub': 'refresh_token',
        }
        access_token = jwt.encode(
            access_payload,
            JWT_SECRET,
            algorithm=JWT_ALGO
        )
        refresh_token = jwt.encode(
            refresh_payload,
            JWT_SECRET,
            algorithm=JWT_ALGO
        )
        token_response = {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
        # Save refresh token in db
        user = get_user_model().objects.get(email=email)
        refresh_token_object, _ = RefreshToken.objects.get_or_create(user=user)
        refresh_token_object.refresh_token = refresh_token
        refresh_token_object.save()

        return token_response

    def decode_token(self, token):
        """
        Decode JWT tokens.
        """
        decoded_token = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGO]
        )
        return decoded_token

    def refresh_tokens(self, refresh_token):
        """
        Generate new access and refresh tokens after access token expires.
        This function implements refresh token rotation.

        Returns None if refresh token is invalid.
        """
        decoded_refresh_token = self.decode_token(refresh_token)
        email = decoded_refresh_token['email']
        user = get_user_model().objects.get(email=email)
        refresh_token_object = RefreshToken.objects.get(user=user)
        if decoded_refresh_token['sub'] != 'refresh_token':
            return None
        if decoded_refresh_token['exp'] < time.time():
            # Refresh token has expired.
            return None
        elif refresh_token != refresh_token_object.refresh_token:
            # Refresh token is not the user's latest one.
            return None
        else:
            # Refresh token is valid.
            new_tokens = self.encode_tokens(
                email=decoded_refresh_token['email'])
            # Save refresh token in db
            refresh_token_object.refresh_token = new_tokens['refresh_token']
            refresh_token_object.save()
            return new_tokens
