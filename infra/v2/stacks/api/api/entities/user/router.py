from fastapi import APIRouter, status

import api.entities.user.logic as logic
from api.entities.user.models import UserInput, UserOutput

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(user: UserInput) -> UserOutput:
    user_out = logic.create_new_user(user)
    return user_out
