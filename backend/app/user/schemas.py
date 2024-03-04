"""
Schemas for apis in user app.
"""
from django.contrib.auth import get_user_model
from ninja import ModelSchema, Schema
from typing import Optional


class UserSchemaIn(Schema):
    """Input Schema for user model."""
    email: str
    password: str
    first_name: str = ''
    last_name: str = ''


class UserSchemaOut(Schema):
    """Output Schema for user model."""
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class PatchUserSchema(ModelSchema):
    """Input for updating user model."""
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']
        fields_optional = ['first_name', 'last_name']


class CredentialsSchema(Schema):
    """Input Schema for user credentials."""
    email: str
    password: str


class ChangePasswordSchema(Schema):
    """Input Schema for change_password."""
    old_password: str
    new_password: str


class TokenSchema(Schema):
    """Output Schema for the token api."""
    access_token: str
    refresh_token: str


class RefreshSchema(Schema):
    """Input Schema for refreshing tokens."""
    refresh_token: str


class ErrorSchema(Schema):
    """Output Schema for errors."""
    message: str
