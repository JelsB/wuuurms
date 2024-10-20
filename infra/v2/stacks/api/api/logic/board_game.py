from api.data_access.ddb_client import DdbClient
from api.models.board_game import BoardGameInDdb, BoardGameInput
from api.settings import table_name


def create_board_game(board_game: BoardGameInput):
    ddb_client = DdbClient(table_name().board_game)
    board_game_db = BoardGameInDdb(**board_game.model_dump())
    ddb_client.put_item(board_game_db.model_dump())

    return board_game_db
