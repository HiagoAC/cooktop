"""
Tests for auth_handler.
"""
import jwt
import time

from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from user.auth_handler import (
    AuthHandler,
    InvalidAccessTokenError,
    InvalidRefreshTokenError,
    JWT_SECRET,
    JWT_ALGO
)


class AuthHandlerTests(TestCase):
    """Tests for AuthHandler."""

    def setUp(self):
        self.auth_handler = AuthHandler()
        self.email = 'test@example.com'
        self.user = get_user_model().objects.create(
            email='test@example.com',
            password='password321'
        )
        factory = RequestFactory()
        self.request = factory.get('/any-url/')

    def test_authenticate_with_valid_token(self):
        """Test authenticating user with a valid token."""
        tokens = self.auth_handler.encode_tokens(email=self.email)
        auth_user = self.auth_handler.authenticate(
            self.request, tokens['access_token'])

        self.assertIsInstance(auth_user, get_user_model())
        self.assertEqual(auth_user, self.user)

    def test_authenticate_as_user_that_doesnt_exist(self):
        """
        Test that None is return when attempting to authenticate
        with a token with an email that does not belong to a user.
        """
        payload = {
            'email': 'thisUserDoesNotExist@email.com',
            'exp': time.time() + timedelta(minutes=10).total_seconds(),
            'sub': 'access_token',
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)
        with self.assertRaises(InvalidAccessTokenError):
            self.auth_handler.authenticate(self.request, token)

    def test_endcode_tokens_returns_tokens(self):
        """
        Test encode_tokens method responds with
        distinct access and refresh tokens.
        """
        response = self.auth_handler.encode_tokens(email=self.email)

        self.assertIsNotNone(response['access_token'])
        self.assertIsNotNone(response['refresh_token'])
        self.assertNotEqual(
            response['access_token'],
            response['refresh_token']
        )

    def test_encode_decode_tokens(self):
        """
        Test that data is correct after encoding and
        decoding a token.
        """
        response = self.auth_handler.encode_tokens(email=self.email)
        decoded_access_token = self.auth_handler.decode_token(
            response['access_token'])
        decoded_refresh_token = self.auth_handler.decode_token(
            response['refresh_token'])

        self.assertEqual(decoded_access_token['email'], self.email)
        self.assertEqual(decoded_refresh_token['email'], self.email)
        self.assertEqual(decoded_access_token['sub'], 'access_token')
        self.assertEqual(decoded_refresh_token['sub'], 'refresh_token')

    def test_refresh_tokens_with_valid_token(self):
        """
        Test that tokens are refreshed when calling the method
        refresh_tokens with a valid refresh token.
        """
        old_tokens = self.auth_handler.encode_tokens(email=self.email)
        new_tokens = self.auth_handler.refresh_tokens(
            old_tokens['refresh_token'])

        self.assertIsNotNone(new_tokens['access_token'])
        self.assertIsNotNone(new_tokens['refresh_token'])
        self.assertNotEqual(new_tokens['access_token'],
                            old_tokens['access_token'])
        self.assertNotEqual(new_tokens['refresh_token'],
                            old_tokens['refresh_token'])

    def test_refresh_tokens_with_wrong_token_type(self):
        """
        Test that calling refresh_token with token of a type that is
        not refresh_token raises InvalidTokenError.
        """
        tokens = self.auth_handler.encode_tokens(email=self.email)
        with self.assertRaises(InvalidRefreshTokenError):
            self.auth_handler.refresh_tokens(tokens['access_token'])

    def test_refresh_tokens_with_not_latest_refresh_token(self):
        """
        Test that calling refresh_tokens with a token that is not the user's
        latest refresh token raises InvalidRefreshTokenError.
        """
        old_tokens = self.auth_handler.encode_tokens(email=self.email)
        self.auth_handler.encode_tokens(email=self.email)
        with self.assertRaises(InvalidRefreshTokenError):
            self.auth_handler.refresh_tokens(old_tokens['refresh_token'])
