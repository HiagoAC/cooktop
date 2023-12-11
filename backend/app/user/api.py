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

from user.auth_handler import AuthHandler
from user.schemas import (
    UserSchemaIn,
    UserSchemaOut,
    CredentialsSchema,
    TokenSchema,
    ErrorSchema,
)

user_router = Router()
token_router = Router()


@user_router.post('/', response={
    201: UserSchemaOut, 409: ErrorSchema, 422: ErrorSchema
    }, url_name='create_user', auth=None)
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


@user_router.get('/me', response={200: UserSchemaOut}, url_name='user_me')
def user_me(request):
    """Retrieves user's data in User model."""
    user = request.auth
    return UserSchemaOut.from_orm(user)


@token_router.post('/', response={200: TokenSchema, 401: ErrorSchema},
                   url_name='get_token', auth=None)
def get_token(request, payload: CredentialsSchema):
    """Get access and refresh tokens."""
    user = authenticate(
        email=payload.email,
        password=payload.password,
    )
    if not user:
        return 401, {'message': 'Invalid credentials.'}
    auth_handler = AuthHandler()
    tokens = auth_handler.encode_tokens(email=payload.email)
    return 200, tokens
