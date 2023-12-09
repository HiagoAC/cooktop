"""
/users/ API views.
"""
from django.contrib.auth import ( # noqa
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _ # noqa

from ninja import Router

from user.schemas import UserSchemaIn, UserSchemaOut

router = Router()


@router.post('/', response={201: UserSchemaOut})
def create_user(request, payload: UserSchemaIn):
    """Create a user."""
    get_user_model().objects.create_user(**payload.dict())
    response = payload.dict()
    response.pop('password', None)
    return response
