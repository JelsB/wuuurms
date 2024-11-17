from fastapi import APIRouter, status

import api.entities.player.logic as logic
from api.entities.player.models import PlayerInput, PlayerOutput


router = APIRouter(prefix='/players', tags=['players'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_player(player: PlayerInput) -> PlayerOutput:
    player_out = logic.create_new_player(player)
    return player_out
