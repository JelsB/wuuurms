1. `mkdir infra`
2. `cd infra`
3. `cdk init --language=python`
4. `cd -`
5. `flutter create app`

Testing
1. `cd app`
2. `flutter run`
   1.  shows linux and chrome automatically detected options
   2.   Enable debug mode on phone (click build status 7 times + enable it). Plug in phone. `flutter run` automatically builds and opens app on phone.

1. Add amplify packages
   1. add to pubspec.yaml
   2. run `flutter pub get`
2. Update platform configurations
   1. android
3. `amplify init`
   1. Select CloudFormation
   2. Select profile with `AdministratorAccess-Amplify` policy permission
   3. If you can an error `You have reached the Amplify App limit for this account and region`. Delete all amplify apps and try again.
   4. Deploys a CloudFormation stack
      1.  2 IAM roles
      2.  S3 bucket
   5. Deploys an Amplify application
   6. Creates `amplify/` folder
      1. `team-provider-info.json` contains info about CloudFormation stacks and its resources
      2. a bunch of files/folders that should not be version controlled (see `.gitignore`)
   7. `amplify add api`
      1. select GraphQL
      2. Select AWS Incognito for authorisation
         1. Use default configuration
         2. Login with Username
      3. This updates `amplify/backend/backend-config.json` file with login configuration
      4. This creates `amplifybackend/auth/<app_name_suffix` folder with `cli-inputs.json` file which contains Congnito configuration.
      5. Enter `N` when prompted to Configure additional auth types
      6. Select Continue
      7. Add blank schema
      8. Select Y to edit schema
         ```
         type BudgetEntry @model @auth(rules: [{ allow: owner }]) {
         id: ID!
         title: String!
         description: String
         amount: Float!
         }
         ```
      9. `amplify push`
         1.  Updates existing stack with lambda function, role, and custom resource + 2 nested stacks
         2.  First nested stack: auth/cognito related resources
         3.  Second nested stack: AppSync GraphQL api, schema and Datasource + 2 more nested stacks
             1.  First nested stack: AppSync resolvers and function configurations
             2.  Second nested stack: empty
         4.  It returns your GraphQL endpoint and transform version
      10. `amplify codegen models` creates Dart model files based on GraphQL schema  

# Platform configuration updates
See docs for all platforms: https://docs.amplify.aws/start/getting-started/setup/q/integration/flutter/#platform-setup
## Android
Amplify requires a minimum of API level 24 (Android 7.0), Gradle 7 and Kotlin > 1.7 when targeting Android.

From your project root, navigate to the android/ directory and open build.gradle in the text editor of your choice. Update the Gradle plugin version to 7.4.2 or higher:
```
dependencies {
-       classpath 'com.android.tools.build:gradle:7.2.0'
+       classpath 'com.android.tools.build:gradle:7.4.2'
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"
    }
``` 
If your Kotlin Gradle plugin version is below 1.7, update android/build.gradle:
```
ext.kotlin_version = '1.7.10'
```
Then, open android/gradle/wrapper/gradle-wrapper.properties. Update the Gradle distributionUrl to a version between 7.3 and 7.6.1 (see the Flutter docs for more info).
```
-distributionUrl=https\://services.gradle.org/distributions/gradle-7.0-all.zip
+distributionUrl=https\://services.gradle.org/distributions/gradle-7.6.1-all.zip
```
Then, open android/app/build.gradle. Update the minimum Android SDK version to 24 or higher:
```
defaultConfig {
        // TODO: Specify your own unique Application ID (https://developer.android.com/studio/build/application-id.html).
        applicationId "com.example.myapp"
        // You can update the following values to match your application needs.
        // For more information, see: https://docs.flutter.dev/deployment/android#reviewing-the-gradle-build-configuration.
-       minSdkVersion flutter.minSdkVersion
+       minSdkVersion 24
        targetSdkVersion flutter.targetSdkVersion
        versionCode flutterVersionCode.toInteger()
        versionName flutterVersionName
    }
```