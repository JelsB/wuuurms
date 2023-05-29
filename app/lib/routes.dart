// GoRouter configuration
import 'package:amplify_authenticator/amplify_authenticator.dart';
import 'package:app/models/BudgetEntry.dart';
import 'package:app/screens/home.dart';
import 'package:app/screens/manage_budget_entry.dart';
import 'package:app/screens/profile.dart';
import 'package:go_router/go_router.dart';

final router = GoRouter(routes: [
  GoRoute(
    path: '/',
    builder: (context, state) => const HomeScreen(),
  ),
  GoRoute(
    path: '/manage-budget-entry',
    name: 'manage',
    builder: (context, state) => ManageBudgetEntryScreen(
      budgetEntry: state.extra as BudgetEntry?,
    ),
  ),
  GoRoute(
      path: '/login',
      name: 'login',
      builder: (context, state) =>
          const AuthenticatedView(child: ProfileScreen()))
]);
