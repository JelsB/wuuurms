from pathlib import Path

from aws_cdk import Duration, Stack
from aws_cdk.aws_apigateway import EndpointConfiguration, EndpointType, LambdaRestApi
from aws_cdk.aws_lambda import LayerVersion, Runtime, Tracing
from aws_cdk.aws_lambda_python_alpha import BundlingOptions, PythonFunction
from aws_cdk.aws_logs import RetentionDays
from constructs import Construct


class ApiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = self.create_api()
        self.create_api_gateway(api)

    def create_api(self):
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

        return api

    def create_api_gateway(self, api):
        LambdaRestApi(
            self, 'ApiGateway', handler=api, endpoint_configuration=EndpointConfiguration(types=[EndpointType.REGIONAL])
        )
