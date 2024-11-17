from fastapi import APIRouter, HTTPException, status

from api.common_router.responses import HTTP_RESPONSES
import api.entities.player.logic as logic
from api.entities.player.models import PlayerInput, PlayerOutput
from api.exceptions import DatabaseException


router = APIRouter(prefix='/players', tags=['players'], responses=HTTP_RESPONSES[status.HTTP_500_INTERNAL_SERVER_ERROR])


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_player(player: PlayerInput) -> PlayerOutput:
    try:
        player_out = logic.create_new_player(player)
        return player_out
    except DatabaseException:
        raise HTTPException(status_code=500, detail='Internal server error')
