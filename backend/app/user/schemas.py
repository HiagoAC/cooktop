"""
Schemas for the user API.
"""
from django.contrib.auth import get_user_model
from ninja import ModelSchema


class UserSchemaIn(ModelSchema):
    """INPUT Schema for user model."""
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']
        optional_fields = ['first_name', 'last_name']


class UserSchemaOut(ModelSchema):
    """OUTPUT Schema for user model."""
    class Meta:
        model = get_user_model()
        fields = ['email']
        optional_fields = ['first_name', 'last_name', ]
