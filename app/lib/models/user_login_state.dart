import 'dart:async';

import 'package:amplify_flutter/amplify_flutter.dart';
import 'package:flutter/material.dart';

class UserLoginStateModel extends ChangeNotifier {
  bool loggedIn = false;
  StreamSubscription<AuthHubEvent>? subscription;

  UserLoginStateModel() {
    _getInitialUserLoginState();
    _listenToAuthenticationEvent();
  }

  static Future<bool> _isUserSignedIn() async {
    try {
      final result = await Amplify.Auth.fetchAuthSession();
      safePrint('User is signed in: ${result.isSignedIn}');
      return result.isSignedIn;
    } on AuthException catch (e) {
      safePrint('Error retrieving auth session: ${e.message}');
      return false;
    }
  }

  void changeTo(bool newLoginState) {
    loggedIn = newLoginState;
    notifyListeners();
  }

  Future<void> _getInitialUserLoginState() async {
    loggedIn = await _isUserSignedIn();
  }

  void _listenToAuthenticationEvent() {
    subscription = Amplify.Hub.listen(HubChannel.Auth, (AuthHubEvent event) {
      switch (event.type) {
        case AuthHubEventType.signedIn:
          safePrint('User is signed in.');
          changeTo(true);
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
