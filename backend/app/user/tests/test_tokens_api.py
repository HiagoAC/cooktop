"""
Tests for the tokens API.
"""
import json
import jwt
import time

from datetime import timedelta
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client, TestCase

from user.auth_handler import JWT_SECRET, JWT_ALGO
from user.models import RefreshToken


TOKEN_URL = reverse('api:get_tokens')
REFRESH_URL = reverse('api:refresh_tokens')


class TokensAPITests(TestCase):
    """Tests for the tokens api."""

    def setUp(self):
        self.client = Client()

    def encode_token(self, payload):
        """Encode JWT tokens."""
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

    def test_create_token_for_user(self):
        """Test generating a token with valid credentials."""
        payload = {
            'email': 'test@example.com',
            'password': 'password321',
        }
        get_user_model().objects.create_user(**payload)
        response = self.client.post(
                TOKEN_URL,
                data=json.dumps(payload),
                content_type='application/json',
            )
        # 200 - OK
        self.assertEqual(response.status_code, 200)

        # Parse content
        content = json.loads(response.content.decode('utf-8'))

        self.assertIn('access_token', content)
        self.assertIn('refresh_token', content)

    def test_create_token_with_bad_credentials(self):
        """Test requesting a token with bad credentials returns an error."""
        email = 'test@example.com'
        good_pass = 'goodpassword321'
        bad_pass = 'badpassword321'

        get_user_model().objects.create_user(
            email=email,
            password=good_pass,
        )

        payload = {
            'email': email,
            'password': bad_pass,
        }

        response = self.client.post(
                        TOKEN_URL,
                        data=json.dumps(payload),
                        content_type='application/json',
                    )

        # Parse content
        content = json.loads(response.content.decode('utf-8'))

        self.assertNotIn('token', content)

    def test_refresh_tokens(self):
        """Test refreshing tokens with a valid refresh token."""
        email = 'test@example.com'
        user = get_user_model().objects.create(email=email)
        token_data = {
            'email': email,
            'exp':  time.time() + timedelta(days=7).total_seconds(),
            'sub': 'refresh_token'
        }
        token = self.encode_token(token_data)
        RefreshToken.objects.create(user=user, refresh_token=token)
        response = self.client.post(
                        REFRESH_URL,
                        data=json.dumps({'refresh_token': token}),
                        content_type='application/json',
                    )

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        # Parse content
        content = json.loads(response.content.decode('utf-8'))

        self.assertIn('access_token', content)
        self.assertIn('refresh_token', content)

    def test_refresh_tokens_with_token_that_cant_be_decoded(self):
        """
        Test that requesting updated tokens with a token that cannot be
        decoded returns an error.
        """
        email = 'test@example.com'
        user = get_user_model().objects.create(email=email)

        bad_token = 'this_token_cannot_be_decoded'
        RefreshToken.objects.create(
            user=user, refresh_token=bad_token)
        response = self.client.post(
            REFRESH_URL,
            data=json.dumps(
                {'refresh_token': bad_token}),
            content_type='application/json')

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)

    def test_refresh_tokens_with_expired_token(self):
        """
        Test that requesting updated tokens with an expired token returns
        an error.
        """
        email = 'test@example.com'
        user = get_user_model().objects.create(email=email)

        expired_token = self.encode_token({
            'email': email,
            'exp': time.time() - timedelta(days=7).total_seconds(),
            'sub': 'refresh_token',
        })
        RefreshToken.objects.create(
            user=user, refresh_token=expired_token)
        response = self.client.post(
            REFRESH_URL,
            data=json.dumps(
                {'refresh_token': expired_token}),
            content_type='application/json')

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)

    def test_refresh_tokens_with_wrong_token_type(self):
        """
        Test that requesting updated tokens with a token that is not a refresh
        token returns an error.
        """
        email = 'test@example.com'
        user = get_user_model().objects.create(email=email)

        not_refresh_token = self.encode_token({
            'email': email,
            'exp': time.time() + timedelta(days=7).total_seconds(),
            'sub': 'access_token'
        })
        RefreshToken.objects.create(
            user=user, refresh_token=not_refresh_token)
        response = self.client.post(
            REFRESH_URL,
            data=json.dumps(
                {'refresh_token': not_refresh_token}),
            content_type='application/json')

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)

    def test_refresh_tokens_with_not_latest_token(self):
        """
        Test that requesting updated tokens with a token that is not the latest
        token returns an error.
        """
        email = 'test@example.com'
        user = get_user_model().objects.create(email=email)

        not_latest_token = self.encode_token({
            'email': email,
            'exp': time.time() + timedelta(days=7).total_seconds(),
            'sub': 'refresh_token'
        })
        RefreshToken.objects.create(
            user=user, refresh_token='latest_token')
        response = self.client.post(
            REFRESH_URL,
            data=json.dumps(
                {'refresh_token': not_latest_token}),
            content_type='application/json')

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)
