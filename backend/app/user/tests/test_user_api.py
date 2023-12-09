"""
Tests for the user API.
"""
import json

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse

from http import HTTPStatus as status


CREATE_USER_URL = reverse('api:create_user')
TOKEN_URL = 'api/token'
# ME_URL = 'users'


class PublicUserAPITests(TestCase):
    """Test unauthorized requests to user API."""

    def setUp(self):
        self.client = Client()

    def test_create_user(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'password321',
        }
        response = self.client.post(
            CREATE_USER_URL,
            data=json.dumps(payload),
            content_type='application/json'
        )

        # 201 - CREATED
        self.assertEqual(response.status_code, status.CREATED)
        self.assertTrue(b'password' not in response.content)
        try:
            get_user_model().objects.get(email=payload['email'])
        except ObjectDoesNotExist:
            self.fail(f'user: {payload["email"]} not created.')

    def test_create_user_with_already_used_email(self):
        """Test creating a user with email already in use returns an error."""
        payload = {
            'email': 'test@example.com',
            'password': 'password321',
        }
        self.client.post(CREATE_USER_URL, payload)
        response = self.client.post(CREATE_USER_URL, payload)

        # 400 - BAD REQUEST
        self.assertEqual(response.status_code, status.BAD_REQUEST)

    def test_create_user_with_invalid_password(self):
        """Test creating a user with invalid password returns an error."""
        invalid_passwords = ['tooShort9',
                             '987653420470928', 'noNumbersIncluded']
        email = 'email@example.com'
        for password in invalid_passwords:
            response = self.client.post(CREATE_USER_URL,
                                        {'email': email, 'password': password})
            # 400 - BAD REQUEST
            self.assertEqual(response.status_code, status.BAD_REQUEST)

    def test_create_token_for_user(self):
        """Test generating a token with valid credentials."""
        pass

    def test_create_token_with_bad_credentials(self):
        """Test requesting a token with bad credentials returns an error."""
        pass
