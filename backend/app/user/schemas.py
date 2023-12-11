"""
Schemas for the user API.
"""
from ninja import Schema


class UserSchemaIn(Schema):
    """Input Schema for user model."""
    email: str
    password: str
    first_name: str = ''
    last_name: str = ''


class UserSchemaOut(Schema):
    """Output Schema for user model."""
    email: str
    first_name: str = ''
    last_name: str = ''


class CredentialsSchema(Schema):
    """Input Schema for user credentials."""
    email: str
    password: str


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
