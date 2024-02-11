

import random
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import AppSyncResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.shared.types import TypedDict
from aws_lambda_powertools.utilities.typing import LambdaContext

tracer = Tracer()
logger = Logger()
app = AppSyncResolver()


class Player(TypedDict):
    id: str  # noqa AA03 VNE003, required due to GraphQL Schema
    name: str
    score: str

class UpdateScoreInput(TypedDict):
    id: str  # noqa AA03 VNE003, required due to GraphQL Schema
    boardgame_name: str
    placement: int
    number_of_players: int


@app.resolver(type_name="Mutation", field_name="update_player_score")
@tracer.capture_method
def update_score(input: UpdateScoreInput) -> Player:
    logger.info("Updating player score with random integer.", extra={"payload": input})
    random_int = random.randint(1, 100)
    input["score"] = random_int
    return {"id": input["id"], "name": 'PLAYER NAME', "score": random_int}


@logger.inject_lambda_context(correlation_id_path=correlation_paths.APPSYNC_RESOLVER)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
