import 'dart:async';

import 'package:amplify_auth_cognito/amplify_auth_cognito.dart';
import 'package:amplify_flutter/amplify_flutter.dart';
import 'package:flutter/material.dart';

class UserLoginStateModel extends ChangeNotifier {
  bool loggedIn = false;
  bool isAdmin = false;
  StreamSubscription<AuthHubEvent>? subscription;

  UserLoginStateModel() {
    _getInitialUserLoginState();
    _listenToAuthenticationEvent();
  }

  Future<CognitoAuthSession> _fetchCognitoAuthSession() async {
    try {
      final cognitoPlugin =
          Amplify.Auth.getPlugin(AmplifyAuthCognito.pluginKey);
      return await cognitoPlugin.fetchAuthSession();
    } on AuthException catch (e) {
      safePrint('Error retrieving auth session: ${e.message}');
      throw Exception('Failed to fetch auto session');
    }
  }

  // static Future<void> fetchCurrentUserAttributes() async {
  //   try {
  //     final result = await Amplify.Auth.fetchUserAttributes();
  //     for (final element in result) {
  //       safePrint('key: ${element.userAttributeKey}; value: ${element.value}');
  //     }
  //   } on AuthException catch (e) {
  //     safePrint('Error fetching user attributes: ${e.message}');
  //   }
  // }

  void changeTo(bool newLoginState) {
    safePrint('changing login state to $newLoginState');
    loggedIn = newLoginState;
    notifyListeners();
  }

  Future<void> _getInitialUserLoginState() async {
    try {
      final authSession = await _fetchCognitoAuthSession();
      loggedIn = authSession.isSignedIn;
      final idToken = authSession.userPoolTokensResult.value.idToken;
      isAdmin = idToken.groups.contains('admin');
      safePrint('admin:$isAdmin');
      safePrint('logged in:$loggedIn');
      safePrint('username:${CognitoIdToken(idToken).username}');
    } catch (e) {
      safePrint('Failed to fetch Cognito Auth Session');
    }
  }

  void _listenToAuthenticationEvent() {
    subscription = Amplify.Hub.listen(HubChannel.Auth, (AuthHubEvent event) {
      switch (event.type) {
        case AuthHubEventType.signedIn:
          safePrint('User is signed in.');
          changeTo(true);
          _getInitialUserLoginState();
          break;
        case AuthHubEventType.signedOut:
          safePrint('User is signed out.');
          changeTo(false);
          break;
        case AuthHubEventType.sessionExpired:
          safePrint('The session has expired.');
          break;
        case AuthHubEventType.userDeleted:
          safePrint('The user has been deleted.');
          break;
      }
    });
  }
}
