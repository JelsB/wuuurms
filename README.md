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

3. Add amplify packages
   1. add to pubspec.yaml
   2. run `flutter pub get`