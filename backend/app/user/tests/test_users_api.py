"""
Tests for the users API.
"""
import json
import jwt
import time

from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse

from user.auth_handler import JWT_SECRET, JWT_ALGO


CREATE_USER_URL = reverse('api:create_user')
ME_URL = reverse('api:user_me')
CHANGE_PASSWORD_URL = reverse('api:change_password')


class PublicUsersAPITests(TestCase):
    """Test unauthenticated requests to user API."""

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
        self.assertEqual(response.status_code, 201)

        # Parse content
        content = json.loads(response.content.decode('utf-8'))

        self.assertNotIn('password', content)
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
        self.client.post(
            CREATE_USER_URL,
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = self.client.post(
            CREATE_USER_URL,
            data=json.dumps(payload),
            content_type='application/json'
        )

        # 409 - CONFLICT
        self.assertEqual(response.status_code, 409)

    def test_create_user_with_invalid_password(self):
        """Test creating a user with invalid password returns an error."""
        invalid_passwords = ['tooShort9',
                             '987653420470928', 'noNumbersIncluded']
        email = 'email@example.com'
        for password in invalid_passwords:
            payload = {
                'email': email,
                'password': password,
            }
            response = self.client.post(
                CREATE_USER_URL,
                data=json.dumps(payload),
                content_type='application/json',
            )
            # 422 - UNPROCESSABLE ENTITY
            self.assertEqual(response.status_code, 422)

    def test_retrieve_user_unauthorized(self):
        """"
        Test that retrieving user without authentication is unauthorized.
        """
        response = self.client.get(ME_URL)

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)


class PrivateUsersAPITests(TestCase):
    """Test authenticated requests for the user api."""

    def setUp(self):
        self.email = 'test@example.com'
        self.first_name = 'John'
        self.last_name = 'Doe'
        self.password = 'password321'
        self.user = get_user_model().objects.create_user(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name
        )
        token_data = {
            'email': self.email,
            'exp': time.time() + timedelta(minutes=10).total_seconds(),
            'sub': 'access_token',
        }
        access_token = jwt.encode(token_data, JWT_SECRET, algorithm=JWT_ALGO)
        self.client = Client()
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

    def test_retrieve_user_authorized(self):
        """Tests that retrieving own user data is successful."""
        response = self.client.get(ME_URL, **self.headers)

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        # Parse content
        content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(content['email'], self.email)
        self.assertEqual(content['first_name'], self.first_name)
        self.assertEqual(content['last_name'], self.last_name)
        self.assertNotIn('password', content)

    def test_update_user(self):
        """Test updating user fields."""
        payload = {
            'first_name': 'new_name',
            'last_name': 'new_last_name',
        }
        response = self.client.patch(
            ME_URL,
            **self.headers,
            data=json.dumps(payload),
            content_type='application/json'
        )

        # 200 - OK
        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()

        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertEqual(self.user.last_name, payload['last_name'])

    def test_update_user_email(self):
        """Test updating user email fails."""
        email = self.user.email
        payload = {
            'email': 'another_email@example.com'
        }
        self.client.patch(
            ME_URL,
            **self.headers,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.user.refresh_from_db()

        self.assertEqual(self.user.email, email)

    def test_update_user_password_wrong_endpoint(self):
        """Test updating user password through update_user fails."""
        payload = {
            'password': 'newPass123456789'
        }
        self.client.patch(
            ME_URL,
            **self.headers,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.user.refresh_from_db()

        self.assertFalse(self.user.check_password(payload['password']))

    def test_update_user_password_wrong_old_password(self):
        """Test updating user password with wrong old password."""
        payload = {
            'old_password': 'anotherPass',
            'new_password': 'newPass123456789'
        }
        response = self.client.patch(
            CHANGE_PASSWORD_URL,
            **self.headers,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.user.refresh_from_db()

        # 401 - UNAUTHORIZED
        self.assertEqual(response.status_code, 401)
        self.assertFalse(self.user.check_password(payload['new_password']))

    def test_update_user_password_correct(self):
        """Test updating user password."""
        payload = {
            'old_password': self.password,
            'new_password': 'newPass123456789'
        }
        response = self.client.patch(
            CHANGE_PASSWORD_URL,
            **self.headers,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.user.refresh_from_db()

        # 200 - NO CONTENT
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b'')
        self.assertTrue(self.user.check_password(payload['new_password']))
