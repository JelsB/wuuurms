from fastapi import APIRouter, status

from api.entities.board_game.logic import create_new_board_game
from api.entities.board_game.models import BoardGameInput, BoardGameOutput


router = APIRouter(prefix='/board-games', tags=['board games'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_board_game(board_game: BoardGameInput) -> BoardGameOutput:
    board_game_out = create_new_board_game(board_game)
    return board_game_out
