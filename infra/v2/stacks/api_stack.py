from pathlib import Path
from typing import TypedDict

from aws_cdk import Duration, Stack
from aws_cdk.aws_apigateway import EndpointConfiguration, EndpointType, LambdaRestApi
from aws_cdk.aws_dynamodb import ITableV2
from aws_cdk.aws_lambda import LayerVersion, Runtime, Tracing
from aws_cdk.aws_lambda_python_alpha import BundlingOptions, PythonFunction
from aws_cdk.aws_logs import RetentionDays
from constructs import Construct

from stacks.databases_stack import Tables


class ApiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, tables: Tables, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = self.create_api(tables)
        self.create_api_gateway(api)

    def create_api(self, tables: Tables):
        lambdaPowerToolsLayer = LayerVersion.from_layer_version_arn(
            self,
            'LambdaPowerToolsLayer',
            f'arn:aws:lambda:{self.region}:017000801446:layer:AWSLambdaPowertoolsPythonV3-python312-x86_64:2',
        )

        api = PythonFunction(
            self,
            'Api',
            function_name='api',
            description='The API of the Wuuurms applications.',
            runtime=Runtime.PYTHON_3_12,
            entry=str(Path(__file__).parent / 'api'),
            index='api/handlers/main.py',
            handler='lambda_handler',
            bundling=BundlingOptions(asset_excludes=['tests/', '**/*cache*/', '*.md', '.vscode/']),
            environment={'POWERTOOLS_SERVICE_NAME': 'api'},
            timeout=Duration.seconds(5),
            log_retention=RetentionDays.TWO_WEEKS,
            tracing=Tracing.ACTIVE,
            layers=[lambdaPowerToolsLayer],
        )

        # TODO: temp cause only using dev environment at the moment
        api.add_environment('ENVIRONMENT', 'dev')

        tables['board_game_table'].grant_read_write_data(api)
        api.add_environment('TABLE_NAME_BOARD_GAME', tables['board_game_table'].table_name)

        return api

    def create_api_gateway(self, api):
        LambdaRestApi(
            self, 'ApiGateway', handler=api, endpoint_configuration=EndpointConfiguration(types=[EndpointType.REGIONAL])
        )
