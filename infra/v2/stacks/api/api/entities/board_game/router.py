from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Query, status
from pydantic import UUID4  # , BaseModel

import api.entities.board_game.logic as logic
from api.entities.board_game.models import BoardGameInput, BoardGameOutput, GetBoardGameOutput, ListFilterParams
from api.exceptions import DatabaseException, ItemNotFound


router = APIRouter(prefix='/board-games', tags=['board games'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_board_game(board_game: BoardGameInput) -> BoardGameOutput:
    board_game_out = logic.create_new_board_game(board_game)
    return board_game_out


# Add model to create openApi documentation for 404 response
# class HTTP_404_Model(BaseModel):
#     detail: str


@router.get(
    '/{id}'
    # for openApi documentation
    # responses={404: {'description': 'Board game not found', 'model': HTTP_404_Model}}
)
def get_board_game(
    id: Annotated[UUID4, Path(title='Unique identifier of the board game to retrieve')],
) -> GetBoardGameOutput:
    try:
        out = logic.get_board_game(str(id))
        return out
    except ItemNotFound:
        raise HTTPException(status_code=404, detail='Board game not found.')
    except DatabaseException:
        raise HTTPException(status_code=500, detail='Internal server error')


@router.get('/')
def get_board_games(query_params: Annotated[ListFilterParams, Query()]) -> list[GetBoardGameOutput]:
    start_board_game: logic.BoardGameToStartFrom | None = None
    if query_params.start_name and query_params.start_id:
        start_board_game = {'name': query_params.start_name, 'pk': str(query_params.start_id)}
    print(query_params)
    out = logic.get_board_games_by_name(
        limit=query_params.limit, ordering=query_params.order_by_name, start_board_game=start_board_game
    )
    return out


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_board_game(id: Annotated[UUID4, Path(title='Unique identifier of the board game to delete')]):
    logic.delete_board_game(str(id))
    return {'message': f'Board game with id {id} was successfully deleted.'}
