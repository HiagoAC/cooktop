"""
/users/ API views.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils.translation import gettext as _ # noqa

from ninja import Router

from user.schemas import (
    UserSchemaIn,
    UserSchemaOut,
    CredentialsSchema,
    TokenSchema,
    ErrorSchema,
)

user_router = Router()
token_router = Router()


@user_router.post(
        '/',
        response={
            201: UserSchemaOut,
            409: ErrorSchema,
            422: ErrorSchema,
        }, url_name='create_user')
def create_user(request, payload: UserSchemaIn):
    """Create a user."""
    try:
        get_user_model().objects.create_user(**payload.dict())
    except ValidationError as e:
        return 422, {'message': str(e)}
    except IntegrityError as e:
        return 409, {'message': str(e)}

    response = payload.dict()
    response.pop('password', None)
    return 201, response


@token_router.post(
        '/',
        response={
            200: TokenSchema,
            401: ErrorSchema,
        }, url_name='get_token')
def get_token(request, payload: CredentialsSchema):
    """Get an auth token."""
    user = authenticate(
        email=payload.email,
        password=payload.password,
    )
    if not user:
        return 401, {'message': 'Invalid credentials.'}
    return 200, {'access_token': 'dummy', 'refresh_token': 'dummy'}
