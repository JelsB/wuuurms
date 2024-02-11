import * as cdk from 'aws-cdk-lib'
import * as lambda from 'aws-cdk-lib/aws-lambda'
import { Construct } from 'constructs'
import { AmplifyGraphqlApi, AmplifyGraphqlDefinition } from '@aws-amplify/graphql-api-construct'
import * as path from 'path'
import { CfnUserPoolGroup, UserPool, UserPoolClient } from 'aws-cdk-lib/aws-cognito'
import { IdentityPool, UserPoolAuthenticationProvider } from '@aws-cdk/aws-cognito-identitypool-alpha'
import { Role, WebIdentityPrincipal } from 'aws-cdk-lib/aws-iam'
import assert from 'assert'

/**
 * Contains most of the backend infrastructure.
 */
export class BackendStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: cdk.StackProps) {
    super(scope, id, props)
    assert(props.env, 'props.env is required')

    const userPool = new UserPool(this, 'Pool')
    const userPoolClient = new UserPoolClient(this, 'PoolClient', { userPool: userPool })
    const identityPool = new IdentityPool(this, 'IdentityPool', {
      allowUnauthenticatedIdentities: true,
      authenticationProviders: {
        userPools: [
          new UserPoolAuthenticationProvider({
            userPool,
            userPoolClient,
          }),
        ],
      },
    })

    // This is the same role that gets created when adding an admin
    // user with the Amplify CLI.
    const adminRole = new Role(this, 'AdminRole', {
      assumedBy: new WebIdentityPrincipal('cognito-identity.amazonaws.com', {
        StringEquals: { 'cognito-identity.amazonaws.com:aud': identityPool.identityPoolId },
        'ForAnyValue:StringLike': { 'cognito-identity.amazonaws.com:amr': 'authenticated' },
      }),
    })
    const admins = new CfnUserPoolGroup(this, 'AdminGroup', {
      userPoolId: userPool.userPoolId,
      groupName: 'admins',
      description: 'Admins of the application',
      roleArn: adminRole.roleArn,
    })
    // explicitly add a dependency on the role so that the group is created after the role
    admins.addDependency(adminRole.node.defaultChild as cdk.CfnResource)

    const updatePlayerScoreResolver = new lambda.Function(this, 'UpdatePlayerScoreResolver', {
      functionName: 'update_player_score_resolver',
      runtime: lambda.Runtime.PYTHON_3_12,
      code: lambda.Code.fromAsset(path.join(__dirname, './graphql/resolvers/update_player_score/update_player_score')),
      handler: 'main.lambda_handler',
      description: 'A GraphQL resolver to update the score of a player based on the outcome of a played game.',
      layers: [
        lambda.LayerVersion.fromLayerVersionArn(
          this,
          'AwsLambdaPowertools',
          `arn:aws:lambda:${props.env.region}:017000801446:layer:AWSLambdaPowertoolsPythonV2:61`,
        ),
      ],
    })

    const amplifyApi = new AmplifyGraphqlApi(this, 'GraphQlApi', {
      definition: AmplifyGraphqlDefinition.fromFiles(path.join(__dirname, './graphql/schema.graphql')),
      authorizationModes: {
        defaultAuthorizationMode: 'AMAZON_COGNITO_USER_POOLS',

        iamConfig: {
          identityPoolId: identityPool.identityPoolId,
          authenticatedUserRole: identityPool.authenticatedRole,
          unauthenticatedUserRole: identityPool.unauthenticatedRole,
        },
        userPoolConfig: {
          userPool: userPool,
        },
      },
      functionNameMap: {
        updatePlayerScore: updatePlayerScoreResolver,
      },
    })
  }
}
