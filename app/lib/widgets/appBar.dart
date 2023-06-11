import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

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
    return AppBar(
      title: Text(title),
      actions: [
        TextButton(
          onPressed: () {
            context.pushNamed('boardgames');
          },
          child: const Text(
            'Boardgames',
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

        TextButton(
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
        ...additionalActions, // Spread the additional actions
      ],
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);
}
