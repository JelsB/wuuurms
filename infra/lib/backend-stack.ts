import * as cdk from 'aws-cdk-lib'
import { Construct } from 'constructs'
import { AmplifyGraphqlApi, AmplifyGraphqlDefinition } from '@aws-amplify/graphql-api-construct'
import * as path from 'path'
import { UserPool, UserPoolClient } from 'aws-cdk-lib/aws-cognito'
import { IdentityPool, UserPoolAuthenticationProvider } from '@aws-cdk/aws-cognito-identitypool-alpha'

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
    })
  }
}
