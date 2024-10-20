from os import environ
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from mangum import Mangum
from starlette.requests import Request

from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent

from api.logic.board_game import create_board_game
from api.models.board_game import BoardGameInput, BoardGameOutput
from api.settings import common_env_vars, local_env_vars

local_settings = local_env_vars()
env_vars = common_env_vars()
fast_api_config = {}

# Allow using local swagger UI to test the deployed API in the development environment
if api_id := local_settings.api_id:
    fast_api_config.update({
        'servers': [
            {'url': f'https://{api_id}.execute-api.eu-central-1.amazonaws.com/prod', 'description': 'AWS environment'},
            {'url': '/', 'description': 'Local environment'},
        ]
    })


app = FastAPI(**fast_api_config)

# Allow using local swagger UI to test the deployed API in the development environment
origins = ['http://127.0.0.1:8000'] if env_vars.environment == 'dev' else []

app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'], allow_headers=['*']
)


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
