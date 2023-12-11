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
    PatchUserSchema,
    CredentialsSchema,
    TokenSchema,
    RefreshSchema,
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
def get_user(request):
    """Retrieves user's data in User model."""
    user = request.auth
    return UserSchemaOut.from_orm(user)


@user_router.patch('/me', response={200: UserSchemaOut})
def update_user(request, payload: PatchUserSchema):
    """Updates user fields. Email cannot be updated."""
    user = request.auth
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr == 'password':
            user.set_password(value)
        else:
            setattr(user, attr, value)
    user.save()
    return UserSchemaOut.from_orm(user)


@token_router.post('/', response={
    200: TokenSchema, 401: ErrorSchema}, url_name='get_tokens', auth=None)
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


@token_router.post('/refresh', response={200: TokenSchema},
                   url_name='refresh_tokens', auth=None)
def refresh_tokens(request, payload: RefreshSchema):
    """Get new access and refresh tokens with a valid refresh token."""
    auth_handler = AuthHandler()
    tokens = auth_handler.refresh_tokens(payload.refresh_token)
    return tokens
