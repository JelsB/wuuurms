import 'package:amplify_auth_cognito/amplify_auth_cognito.dart';
import 'package:amplify_flutter/amplify_flutter.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';

import '../models/user_login_state.dart';

class MyAppBar extends StatelessWidget implements PreferredSizeWidget {
  final String title;
  final List<Widget> additionalActions;

  const MyAppBar(
      {super.key, required this.title, this.additionalActions = const []});

  //NOTE: does not work. I think because this is a stateless widget
  // Future<void> _navigateToLogin(context) async {
  //   await context.pushNamed('login');
  //   // // Refresh the entries when returning from the
  //   // // profile screen.
  //   // await _refreshBudgetEntries();
  // }

  @override
  Widget build(BuildContext context) {
    return Consumer<UserLoginStateModel>(
        builder: (context, userLoginState, child) {
      return AppBar(
        title: Text(title, style: const TextStyle(color: Colors.white)),
        backgroundColor: Colors.deepPurple.shade600,
        actions: [
          ...additionalActions, // Spread the additional actions
          TextButton(
            onPressed: () {
              context.pushNamed('boardgames');
            },
            child: const Text(
              'Games',
              style: TextStyle(
                color: Colors.white,
              ),
            ),
          ),
          TextButton(
            onPressed: () {
              context.pushNamed('home');
            },
            child: const Text(
              'Home',
              style: TextStyle(
                color: Colors.white,
              ),
            ),
          ),
          userLoginState.loggedIn
              ? TextButton(
                  onPressed: () {
                    _logOutUser(userLoginState);
                  },
                  child: const Text(
                    'Log out',
                    style: TextStyle(
                      color: Colors.white,
                    ),
                  ),
                )
              : TextButton(
                  onPressed: () {
                    context.pushNamed('login');
                  },
                  child: const Text(
                    'Login',
                    style: TextStyle(
                      color: Colors.white,
                    ),
                  ),
                ),
        ],
      );
    });
  }

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);

  Future<void> _logOutUser(UserLoginStateModel userLoginState) async {
    final result = await Amplify.Auth.signOut();
    if (result is CognitoCompleteSignOut) {
      safePrint('Sign out completed successfully');
      userLoginState.changeTo(false);
    } else if (result is CognitoFailedSignOut) {
      safePrint('Error signing user out: ${result.exception.message}');
    }
  }
}
