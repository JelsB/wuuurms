from typing import Annotated
from fastapi import APIRouter, Path, status
from pydantic import UUID4

import api.entities.board_game.logic as logic
from api.entities.board_game.models import BoardGameInput, BoardGameOutput, GetBoardGameOutput


router = APIRouter(prefix='/board-games', tags=['board games'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_board_game(board_game: BoardGameInput) -> BoardGameOutput:
    board_game_out = logic.create_new_board_game(board_game)
    return board_game_out


@router.get('/{id}')
def get_board_game(
    id: Annotated[UUID4, Path(title='Unique identifier of the board game to retrieve')],
) -> GetBoardGameOutput:
    out = logic.get_board_game(str(id))
    return out
