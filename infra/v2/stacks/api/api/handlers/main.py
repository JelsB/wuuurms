from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from mangum import Mangum
from starlette.requests import Request

from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent

from api.entities.board_game.router import router as board_game_router
from api.entities.player.logic import create_new_player
from api.entities.team.logic import create_new_team
from api.entities.user.logic import create_new_user
from api.entities.board_game.models import BoardGameInput, BoardGameOutput
from api.entities.player.models import PlayerInput, PlayerOutput
from api.entities.team.models import TeamInput, TeamOutput
from api.entities.user.models import UserInput, UserOutput
from api.settings import common_env_vars, local_env_vars

local_settings = local_env_vars()
env_vars = common_env_vars()
fast_api_config = {}

# Allow using local swagger UI to test the deployed API in the development environment
if api_id := local_settings.api_id:
    fast_api_config.update({
        'servers': [
            {'url': '/', 'description': 'Local environment'},
            {'url': f'https://{api_id}.execute-api.eu-central-1.amazonaws.com/prod', 'description': 'AWS environment'},
        ]
    })


app = FastAPI(**fast_api_config)

# Allow using local swagger UI to test the deployed API in the development environment
# TODO move this into infra env var?
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


app.include_router(board_game_router)


@app.post('/users/', status_code=status.HTTP_201_CREATED)
def create_user(user: UserInput) -> UserOutput:
    user_out = create_new_user(user)
    return user_out


@app.post('/players/', status_code=status.HTTP_201_CREATED)
def create_player(player: PlayerInput) -> PlayerOutput:
    player_out = create_new_player(player)
    return player_out


@app.post('/teams/', status_code=status.HTTP_201_CREATED)
def create_team(team: TeamInput) -> TeamOutput:
    team_out = create_new_team(team)
    return team_out


lambda_handler = Mangum(app, lifespan='off')
