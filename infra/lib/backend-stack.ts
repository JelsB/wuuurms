import * as cdk from 'aws-cdk-lib'
import * as lambda from 'aws-cdk-lib/aws-lambda'
import { Construct } from 'constructs'
import { AmplifyGraphqlApi, AmplifyGraphqlDefinition } from '@aws-amplify/graphql-api-construct'
import * as path from 'path'
import { CfnUserPoolGroup, UserPool, UserPoolClient } from 'aws-cdk-lib/aws-cognito'
import { IdentityPool, UserPoolAuthenticationProvider } from '@aws-cdk/aws-cognito-identitypool-alpha'
import { Role, WebIdentityPrincipal } from 'aws-cdk-lib/aws-iam'

/**
 * Contains most of the backend infrastructure.
 */
export class BackendStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props)

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

    const echoLambda = new lambda.Function(this, 'EchoLambda', {
      code: lambda.Code.fromAsset(path.join(__dirname, './graphql/echo')),
      handler: 'index.handler',
      runtime: lambda.Runtime.NODEJS_18_X,
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
        updatePlayerScore: echoLambda,
      },
    })
  }
}
