# Prerequisites
## CDK CLI
Global install should be fine if you don't use this a lot
`npm install -g aws-cdk`
Invoke this with `cdk` command.
Otherwise we use the local version of in project and invoke this with `npx cdk`.

## Flutter
### Install for your platform
https://docs.flutter.dev/get-started/install
### Install dependencies
Run `flutter doctor` to show what you are missing.
#### Android Studio
https://developer.android.com/studio/install and follow OS specific instructions.

#### Android toolchain 
1. `cmdline-tools` via Android Studio IDE or `sdkmanager` cli
2. accept more licenses: `flutter doctor --android-licenses`

#### Other
Other OS specific stuff.

### IDE extensions
https://docs.flutter.dev/get-started/editor

# Run
1. Add `lib/amplifyconfiguration.dart` file
2. `flutter pub get` to install dependencies
3. `flutter run` to run the app
