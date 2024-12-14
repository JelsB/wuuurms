from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Query, status

from api.common_router.responses import HTTP_RESPONSES
import api.entities.user.logic as logic
from api.entities.user.models import CreateUserInput, CreateUserOutput, GetUserOutput, ListFilterParams
from api.exceptions import DatabaseException, ItemNotFound

router = APIRouter(prefix='/users', tags=['users'], responses=HTTP_RESPONSES[status.HTTP_500_INTERNAL_SERVER_ERROR])


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUserInput) -> CreateUserOutput:
    user_out = logic.create_new_user(user)
    return user_out


@router.get('/{username}', responses=HTTP_RESPONSES[status.HTTP_404_NOT_FOUND])
def get_user(username: Annotated[str, Path(title='Username of the User')]) -> GetUserOutput:
    try:
        out = logic.get_user(username)
    except ItemNotFound:
        raise HTTPException(status_code=404, detail=f'User with username {username} was not found.')
    except DatabaseException:
        raise HTTPException(status_code=500, detail='Internal server error')

    return out


@router.get('/')
def get_users(query_params: Annotated[ListFilterParams, Query()]):
    try:
        return logic.get_users(limit=query_params.limit, start_username=query_params.start_username)
    except DatabaseException:
        raise HTTPException(status_code=500, detail='Internal server error')
