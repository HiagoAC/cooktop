"""
API views for the user app.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from ninja import Router
from jwt import ExpiredSignatureError, DecodeError

from user.auth_handler import AuthHandler, InvalidRefreshTokenError
from user.schemas import (
    UserSchemaIn,
    UserSchemaOut,
    PatchUserSchema,
    CredentialsSchema,
    ChangePasswordSchema,
    TokenSchema,
    RefreshSchema,
    ErrorSchema,
)

user_router = Router()
token_router = Router()

create_user_res = {201: UserSchemaOut, 409: ErrorSchema, 422: ErrorSchema}
get_user_res = {200: UserSchemaOut}
update_user_res = {200: UserSchemaOut}
change_password_res = {204: None, 401: ErrorSchema}
get_tokens_res = {200: TokenSchema, 401: ErrorSchema}
refresh_tokens_res = {200: TokenSchema, 401: ErrorSchema}


@user_router.post('/', response=create_user_res,
                  url_name='create_user', auth=None)
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


@user_router.get('/me', response=get_user_res, url_name='user_me')
def get_user(request):
    """Retrieves user's data in User model."""
    user = request.auth
    return UserSchemaOut.from_orm(user)


@user_router.patch('/me', response=update_user_res)
def update_user(request, payload: PatchUserSchema):
    """Updates user fields. Email cannot be updated."""
    user = request.auth
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(user, attr, value)
    user.save()
    return UserSchemaOut.from_orm(user)


@user_router.patch('me/change_password/', response=change_password_res,
                   url_name='change_password')
def change_password(request, payload: ChangePasswordSchema):
    """Changes user password."""
    user = request.auth
    if not user.check_password(payload.old_password):
        return 401, {'message': 'Invalid credentials.'}
    user.set_password(payload.new_password)
    user.save()
    return 204, None


@token_router.post('/', response=get_tokens_res,
                   url_name='get_tokens', auth=None)
def get_tokens(request, payload: CredentialsSchema):
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


@token_router.post('/refresh', response=refresh_tokens_res,
                   url_name='refresh_tokens', auth=None)
def refresh_tokens(request, payload: RefreshSchema):
    """Get new access and refresh tokens with a valid refresh token."""
    auth_handler = AuthHandler()
    try:
        tokens = auth_handler.refresh_tokens(payload.refresh_token)
        return tokens
    except (ExpiredSignatureError, DecodeError, InvalidRefreshTokenError):
        return 401, {'message': 'Invalid token.'}
