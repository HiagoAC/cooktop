"""
Schemas for the user API.
"""
from django.contrib.auth import get_user_model
from ninja import ModelSchema, Schema


class UserSchemaIn(ModelSchema):
    """Input Schema for user model."""
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']
        optional_fields = ['first_name', 'last_name']


class UserSchemaOut(ModelSchema):
    """Output Schema for user model."""
    class Meta:
        model = get_user_model()
        fields = ['email']
        optional_fields = ['first_name', 'last_name', ]


class CredentialsSchema(Schema):
    """Input Schema for user credentials."""
    email: str
    password: str


class TokenSchema(Schema):
    """Output Schema for the token api."""
    access_token: str
    refresh_token: str


class ErrorSchema(Schema):
    """Output Schema for errors."""
    message: str
