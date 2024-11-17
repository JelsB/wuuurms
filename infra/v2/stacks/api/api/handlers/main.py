from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mangum import Mangum
from starlette.requests import Request

from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent

from api.settings import common_env_vars, local_env_vars

from api.entities.board_game.router import router as board_game_router
from api.entities.player.router import router as player_router
from api.entities.team.router import router as team_router
from api.entities.user.router import router as user_router

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

app.include_router(board_game_router)
app.include_router(player_router)
app.include_router(team_router)
app.include_router(user_router)


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


lambda_handler = Mangum(app, lifespan='off')
