from fastapi import FastAPI, status
from mangum import Mangum
from starlette.requests import Request

from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent

from api.logic.board_game import create_board_game
from api.models.board_game import BoardGameInput, BoardGameOutput

app = FastAPI()


@app.get('/ping')
def ping(request: Request):
    # Note: event and context from AWS Lambda Powertools are only available inside the Starlette request.
    # This is different from using the Powertools app event resolvers.
    # This can most likely also be turned into the decorator form. Maybe we need our own one for this.
    event = APIGatewayProxyEvent(request.scope['aws.event'])
    context: LambdaContext = request.scope['aws.context']

    print(f'{event.raw_event=}')
    print(f'{context=}')
    return {'message': 'pong'}


@app.get('/local')
def local():
    """Path for local testing"""
    return {'message': 'local'}


@app.put('/board-game', status_code=status.HTTP_201_CREATED, response_model=BoardGameOutput)
def board_game(board_game: BoardGameInput):
    board_game_out = create_board_game(board_game)
    return board_game_out


lambda_handler = Mangum(app, lifespan='off')
