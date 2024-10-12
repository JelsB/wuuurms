from fastapi import FastAPI
from mangum import Mangum
# from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

app = FastAPI()


@app.get('/ping')
def ping():
    return {'message': 'pong'}


lambda_handler = Mangum(app, lifespan='off')
