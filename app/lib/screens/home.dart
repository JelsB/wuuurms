import 'package:app/widgets/appBar.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
// import 'package:go_router/go_router.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({
    super.key,
  });

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: MyAppBar(
      title: 'App',
      additionalActions: [
        TextButton(
          onPressed: () {
            context.pushNamed('budgets');
          },
          child: const Text(
            'Budgets',
            style: TextStyle(
              color: Colors.white,
            ),
          ),
        ),
      ],
    ));
  }
}
