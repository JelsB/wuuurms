import random
from typing import Dict, cast

import boto3
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import AppSyncResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.shared.types import TypedDict
from aws_lambda_powertools.utilities.typing import LambdaContext

tracer = Tracer()
logger = Logger()
app = AppSyncResolver()


class Player(TypedDict):
    id: str
    name: str
    score: str


class UpdateScoreInput(TypedDict):
    id: str
    boardgame_name: str
    placement: int
    number_of_players: int


class BoardGameScoreParameters(TypedDict):
    base_score: int
    time_multiplier: float
    number_of_players_multiplier: float


class BoardGame(TypedDict):
    id: str
    score_parameters: BoardGameScoreParameters


D: Dict[str, Dict[str, type]] = {
    'time_multiplier': {'N': float},
    'base_score': {'N': int},
    'number_of_players_multiplier': {'N': float},
}

# DDB_BDS: Dict[]


def get_boardgame_scores(boardgame_id: str):
    db_client = boto3.client('dynamodb')

    response = db_client.get_item(
        TableName='BoardGame-hlqs5s7skbadxpmxpoeifvzfny-NONE',
        Key={'id': {'S': boardgame_id}},
        ProjectionExpression='score_parameters',
    )
    board_game = response['Item']
    # sc:  = board_game['score_parameters']['M']
    # values = {k: v['N'] for k, v in sc.items()}

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('BoardGame-hlqs5s7skbadxpmxpoeifvzfny-NONE')
    response2 = table.get_item(Key={'id': boardgame_id})

    item = cast(BoardGame, response2['Item'])
    item['score_parameters']
    pass


def calculate_player_score():
    pass


def update_player_score():
    pass


@app.resolver(type_name='Mutation', field_name='update_player_score')
@tracer.capture_method
def update_score(input: UpdateScoreInput) -> Player:
    get_boardgame_scores(input['boardgame_name'])
    calculate_player_score()
    update_player_score()

    logger.info('Updating player score with random integer.', extra={'payload': input})
    random_int = random.randint(1, 100)
    return {'id': input['id'], 'name': 'PLAYER NAME', 'score': str(random_int)}


@logger.inject_lambda_context(correlation_id_path=correlation_paths.APPSYNC_RESOLVER)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
