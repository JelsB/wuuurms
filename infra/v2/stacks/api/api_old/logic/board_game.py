import uuid
from api_old.data_access.ddb_client import DdbClient
from api_old.models.board_game import BoardGameInDdb, BoardGameInput, BoardGameOutput
from api_old.settings import table_name


def create_new_board_game(board_game: BoardGameInput):
    ddb_client = DdbClient(table_name().board_game)
    board_game_db = BoardGameInDdb(**board_game.model_dump())
    ddb_client.put_item(board_game_db.model_dump())
    board_game_out = BoardGameOutput(id=uuid.UUID(board_game_db.pk, version=4), name=board_game_db.name)
    return board_game_out
