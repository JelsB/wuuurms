import uuid
from typing import Literal, TypedDict

from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb.type_defs import QueryInputTableQueryTypeDef

from api.data_access.ddb_client import DdbClient
from api.entities.board_game.models import BoardGameInDdb, BoardGameInput, BoardGameOutput, GetBoardGameOutput
from api.settings import table_name


def create_new_board_game(board_game: BoardGameInput):
    ddb_client = DdbClient(table_name().board_game)
    board_game_db = BoardGameInDdb(
        **board_game.model_dump(), GSI1PK=f'state#{board_game.state}', GSI1SK=f'name#{board_game.name}'
    )
    ddb_client.put_item(board_game_db.model_dump())
    print(board_game_db.model_dump())
    board_game_out = BoardGameOutput(id=uuid.UUID(board_game_db.pk, version=4), name=board_game_db.name)
    return board_game_out


def get_board_game(id: str):
    ddb_client = DdbClient(table_name().board_game)
    board_game_from_db = ddb_client.get_item_from_pk({'pk': id})
    board_game_out = GetBoardGameOutput(**board_game_from_db)
    return board_game_out


class BoardGameToStartFrom(TypedDict):
    pk: str
    name: str


def get_board_games_by_name(
    start_board_game: BoardGameToStartFrom | None,
    limit: int,
    ordering: Literal['alphabetically', 'reverse alphabetically'],
):
    ddb_client = DdbClient(table_name().board_game)
    query_params: QueryInputTableQueryTypeDef = {
        'IndexName': 'GSI1',
        'KeyConditionExpression': Key('GSI1PK').eq('state#active'),
        'Limit': limit,
        'ScanIndexForward': (ordering == 'alphabetically'),
    }
    if start_board_game:
        query_params['ExclusiveStartKey'] = {
            'pk': start_board_game['pk'],
            'GSI1PK': 'state#active',
            'GSI1SK': f'name#{start_board_game['name']}',
        }

    # TODO: add pagination. This might be necessary if the size of the response is larger than 1MB even when limiting the number of items.
    # DOCS:
    # A single Query operation will read up to the maximum number of items set (if using the Limit parameter)
    # or a maximum of 1 MB of data and then apply any filtering to the results using FilterExpression.
    # If LastEvaluatedKey is present in the response, you will need to paginate the result set.
    # For more information, see Paginating the Results in the Amazon DynamoDB Developer Guide.
    board_games_from_db = ddb_client._ddb_table_client.query(**query_params)

    board_games_out = [
        GetBoardGameOutput(**board_game, id=board_game['pk']) for board_game in board_games_from_db['Items']
    ]
    return board_games_out
