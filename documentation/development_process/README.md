# Description
This document describes the development process. This is useful to figure out what I have learnt and to store and share knowledge later.

# Initialisation
This assumes a local development setup with Flutter is already present. This starts from the [full stack Flutter tutorial of Amplify](https://docs.amplify.aws/start/q/integration/flutter/).

## First steps

1. `mkdir infra`
2. `cd infra`
3. `cdk init --language=python`
4. `cd -`
5. `flutter create app`

## Some testing
1. `cd app`
2. `flutter run`
   1.  shows linux and chrome automatically detected options
   2.   Enable debug mode on phone (click build status 7 times + enable it). Plug in phone. `flutter run` automatically builds and opens app on phone.

## Next steps
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
4.  Add `go_router` package
5.  run `flutter pub get` or VScode does this automatically on saving the `pubspec.yaml` file when Flutter extension is installed.
6.  Replace `main.dart` file with tutorial example
7.  Connect with Amplify auth and api backend services
    1.  Add `auth` (Cognitor) and `api` (GraphQL)
    2.  Replace some code in `main.dart` to configure amplify resources on start-up
8.  run `flutter run`
    1.  Login screen appears before app can be used![Login screen at start-up of app](images/login.png)
    2.  Creating real users with real emails/verification/password etc works out of the box due to Cognito!
        1. Create user `Jels` with fake email address
        2. Create second user `Jels` with real email address
        3. This fails because we choose that usernames have to be unique. The previous user is already stored in Cognito![User Jels with fake email in Cognito](images/cognito_user_jels_fake_email.png)
        4. Manually delete fake user in Cognito
        5. Again create user `Jels` with real email address
        6. Out of the box, it sends verification email with code
        7. Enter received code
        8. You now enter the app's home screen
 9. Add new screen to enter budgets
    1.  Add new class
    2.  Add new route that instantiates this class screen
    3.  Go to this page when pressing `+` button
    4.  `flutter run`
    5.  Press `+` button after login
    6.  Enter budget details
        1.  title: `Test1`
        2.  description:  `some tst`
        3.  amount: `2`
    7.  Submit form
    8.  We are returned to home screen but don't see our newly created budget. It did, however, get created in DynamoDB![item in DynamoDB table with details of newly created budget](images/DDB_first_budget.png)
9.  Show list of budgets on start-up and update when creating new one
    1.  add methos to query the items
    2.  call this method on start-up and after creating new budget
10. Delete items
    1.  add delete GraphQL mutation method
    2.  when swiping away an item, call delete item method
    3.  refresh list after doing that

**This is where the tutorial ends**
## Platform configuration updates
See docs for all platforms: https://docs.amplify.aws/start/getting-started/setup/q/integration/flutter/#platform-setup
### Android
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

# Beyond initial steps
From now on, we build our own application. We do no start from scratch but will adapt the current application we have.

## Add login to specific pages
Instead of adding the login when entering the app/site, it is desirable to already see public information. Login should therefore be an explicit action which shows personal information to the user.

First idea was to call the authenticator after going to the login page but the `Authenticator` component already has the built-in functionality to limit authentication to certain pages. See [the docs](https://ui.docs.amplify.aws/flutter/connected-components/authenticator/customization).

1. We add another route `/login` which requires authentication. Other current routes are public.
> **What have I learnt?** 
> - Routes don't update with *hot reload*. You need to restart the application.
> - `Authenticator` component does not work on Desktop
> - Specific screens for authentication doens't work with `Authenticator`'s `builder` config 

## Add new table
Adding a new DDB table to store boardgames.
1. Manually create new schmema in `amplify/backend/api/hex/schema.graphql`
   1. Start with public one
      ```graphql
      type BoardGame @model {
         id: ID!
         name: String!
         description: String!
         minimumNumberOfPlayers: Int!
         maximumNumberOfPlayers: Int
         minimumDuration: Int!
         maximumDuration: Int
         }
      ```
   2. Run `amplify push`. It will fetch the cloud environment and update resources when needed. Iill show which Cfn stacks will be updated. Here, it wil update the api stack. It will create new resources for our new model.
   3. Run `amplify codegen models` to create the actual models in `lib/models`.
   4. Adapt schema by adding a field with a restricted set of values via an `enum`
      ```
      enum BoardGameType {
         CO_OP,
         WORKER_PLACEMENT
      }

      type BoardGame @model {
         id: ID!
         name: String!
         description: String!
         minimumNumberOfPlayers: Int!
         maximumNumberOfPlayers: Int
         minimumDuration: Int!
         maximumDuration: Int
         type: BoardGameType!
      }
      ```
   5. Run `amplify codegen models` (it can be run before `amplify push`)
   6. Run `amplify push`

> **What have I learnt?** 
> - schema keys cannot contain `-`. Must begin with a letter (`a-z` or `A-Z`) or an underscore (`_`). Names cannot start with a number or any other character.  Following the initial character, names can contain alphanumeric characters (a-z, A-Z, 0-9) and underscores (`_`). Other special characters or symbols are not allowed. It can result in obscure errors on `amplify push`: 
> "There was an error pulling the backend environment dev.
🛑 Syntax Error: Invalid number, expected digit but got: "O".

## All public read access to a table
Goal is to display public access to list of boardgames. A few different approaches were tried before a working solution was found.
### Working solution
1. Specify authentication on the model. Read is public, an owner can do anything.
   ```
   type BoardGame @model @auth(rules: [
      { allow: public, operations: [read],  provider: iam},
      { allow: owner }
      ]) {
   ```
2. Allow unauthenticated users. Change `allowUnauthenticatedIdentities` to `true` in `app/amplify/backend/auth/hex5dfb724f/cli-inputs.json` (see [Not working solution](#not-working-solution) on why using the `amplify` cli directly did not work)
3. Run `amplify push`. This updates the `Amplify Cognito Stack` Cfn stack by updating the Cognito Identidy pool for guests. **TODO:** The unauthenticated IAM role looks the same as the authenticated IAM role. From this, it seems to also allow all CRUD operations. Need to investigate this further.
4. Use `IAM mode` when fetching public items.
   ```dart
   final request = ModelQueries.list(BoardGame.classType,
          authorizationMode: APIAuthorizationType.iam);
   final response = await Amplify.API.query(request: request).response;
   ```
### Not working solution 
- Following the Amplify [docs to add guest access](https://docs.amplify.aws/lib/auth/guest_access/q/platform/flutter/), I ended up with the following configuration:
![Amplify cli commands to try and add guest access](images/try-add-public-auth.png)
Unfortunately, this did not result in the correct solution because it was trying to duplicate IAM configuratation on `amplify push`. Maybe I did something wrong.![Fail to push duplicated IAM configuration via amplify push](images/duplicated-iam-config-public-auth-via-cli.png)

- Using the default authorisation mode for public items does not work. It results in a query exception.
```dart
   final request = ModelQueries.list(BoardGame.classType);
   final response = await Amplify.API.query(request: request).response;
```
Uses no specific authorisation mode in the query request. The default use `AMAZON_COGNITO_USER_POOLS` as specified in `amplify/backend/api/hex/cli-inputs.json`
```
Query failed: UnknownException {
  "message": "unable to send GraphQLRequest to client.",
  "underlyingException": "SignedOutException {\n  \"message\": \"No user is currently signed in\"\n}"
}
``` 
> **What have I learnt?** 
> - Running `amplify pull` can override your local setup with the cloud setup. This is useful when you tried a bunch of local config but cannot undo it do to a number of gitignored files.
> - You need to deploy the IAM authentication mode resources via `amplify push` before you can run queries with the IAM mode. Otherwise you get following error:
> 
> ```
>  Query failed: UnknownException {
>  "message": "unable to send GraphQLRequest to client.",
>  "underlyingException": "SessionExpiredException {\n  \"message\": \"The AWS credentials could not
>  be retrieved\",\n  \"recoverySuggestion\": \"Invoke Amplify.Auth.signIn to re-authenticate the
>  user\",\n  \"underlyingException\": \"NotAuthorizedException {\\n  message=Unauthenticated access
>  is not supported for this identity pool.,\\n}\"\n}"
>  }
>  ```

## Add boardgames via submit form
Goals is to allow admin users to add boardgames.
1. Adding a new `SubmitForm` widget which is deplayed on the boardgames pages.
2. Show buttom to add boardgame when user is logged in


> **What have I learnt?** 
> - Form field controllers are not necessarilty better than `onSaved` callback functions but they make handling nullable types easier I find. Because `onSaved` expects a nullable type but to me, the validator should take care of this being not null (but it also returns a nullable type).
> - Form field controllers cannot be used with the `DropdownButtonFormField`
> - When a logged-in user needs to perform an API call that is public with IAM, be sure to specify that it needs to use `UserPools` instead of IAM.
> - Don't put logic in `createState()` of widgets. The widget parent class is accessible via the `widget` field
> - Excecution a function from a widget which containts another widget can be done by passing the function to the contained widget. This is useful for updating the state of the top level widget after an action of the contained widget.
> - Saving state in asynchronouly in private upon which other aysnc flogic is based is not great. I.e. for knowing if a user is logged in or not. It is not recommended to make the `initState()` method itself async. The `initState()` method is a lifecycle method in Flutter, and it should not be marked as async since it needs to return immediately. Global state management could be a solution.
> - Use `setState()` inside methods when updating state like private variables.
> - using the `late` identifier is not good when dealing with state widgets because
> the variable needs to be initialised before the widget is built (if it uses the variable)

## Beautify UI
Goals:
1. Make app bar dynamic based on the page you are
2. Improve how the grid of boardgames looks like
### Dynamic app bar
Abstracting the app bar into its own widget is pretty straightforward. This widget can have a default layout which can change based on input parameters pass to the constructor when used in other widgets. Currently it's only allow to add more actions when using this app bar widget.
> **What have I learnt?** 
> - The actions on an app bar don't collaps when reducing the window size. I expected it to become a hamburger menu when the screen got smaller.
> - The actions on an app bar don't change how their are displayed based on the platform. I expected it to become a hamburger menu on phone.
> - a Drawer widget is most likely better to use for navigation.
> - To differentiate between platforms, you need to do this explicitly inside widgets. See [docs](https://docs.flutter.dev/ui/layout/building-adaptive-apps#device-segmentation)

### Adaptive grid with images
The screen should look like a grid of image with the title of the game. Temporary goal is to use local image assets and not yet images uploade by a user and stored in S3. The grid should be adaptive when changing the screen size. 

For such a more complex layout, you need to create small modular widget classes.
Adding local assets needs changes in the `pubspec.yaml` file:
```yaml
flutter:

  # To add assets to your application, add an assets section, like this:
  assets:
    - lib/assets/local_tests/boardgame_image/
```

> **What have I learnt?** 
> - To use local assets, you need to add them to `pubspec.yaml`. It only adds assets in the root of the specified directory. When using a directory, you need to end in `/`.
> - To have widgets which can overlay on each other, you can use the `Stack` widget. This was very useful to display the form widget when clicking the floating button.
> - To have control over adaptive layouts such a numner of columns in a grid, you need to wrap your widget in `LayoutBuilder`. This has information about the contraints of the device that is used like the maximum screen width. You can/should then use this to calcultate the number of columns based on the width of your item.

### Create Pop-up with board game details when clicking on it
Make a pop-up appear when clicking on one of the board game tiles. It will display all details of the board game.

I have tried several ways to create a widget that appears on top of the grid when cliking it. One way was to use a Stack and a statemanegent variable, similar to the submission form. But is seems like `Hero` widgets are the better solution for this. They basically create a new screen. This looked more future proof than handling state for N number of board games. I borrowed inspiration for this of from [this video](https://www.youtube.com/watch?v=Bxs8Zy2O4wk) and [code example](https://github.com/funwithflutter/flutter_ui_tips). It creates a custom Router, but the implementation is no too complex. Using `Hero` widgets is pretty straightforward.

The hardest part is still making goor adaptive widget when screen sizes change. I was unable to make the content of the pop-up card wrap correctly when the screen got too small. I tried several combinations of `Wrap`, `Expaneded`, `Row` and `Column`. The problem seems to arise when using `Exapended` and nested `Column`s and `Row`s inside a `Wrap`. I will revisit this, and most likely solve it with `LayoutBuilder`.

> **What have I learnt?** 
> - `Hero` widgets are a cool and easy to use concept. They can be an alternative to `Stack`ed widgets.
> - Enum extensions are a cool feature in Dart!

## Only allow admins to add board games
This needs a new Cognito User Pool group and the permissions need to change in the model.

```
amplify auth update
? What do you want to do?
  Apply default configuration with Social Provider (Federation)
  Walkthrough all the auth configurations
❯ Create or update Cognito user pool groups
? Provide a name for your user pool group: admin
? Do you want to add another User Pool Group - No
? Sort the user pool groups in order of preference …  (Use <shift>+<right/left> to change the order)
✔ Sort the user pool groups in order of preference · admin
```
This add `userPoolGroups` to the `backend-config.json` file. Add `userPoolGroupList` to the `cli-inputs.json` file and creates a new file with `user-pool-group-precedence.json` which now only contains this new user group pool: `admin`.