// GoRouter configuration
import 'package:amplify_authenticator/amplify_authenticator.dart';
import 'package:app/models/BudgetEntry.dart';
import 'package:app/screens/boardgames.dart';
import 'package:app/screens/budgets.dart';
import 'package:app/screens/home.dart';
import 'package:app/screens/manage_budget_entry.dart';
import 'package:app/screens/profile.dart';
import 'package:go_router/go_router.dart';

final router = GoRouter(routes: [
  GoRoute(
      path: '/', name: 'home', builder: (context, state) => const HomeScreen()),
  GoRoute(
    path: '/budgets',
    name: 'budgets',
    builder: (context, state) =>
        const AuthenticatedView(child: BudgetsScreen()),
  ),
  GoRoute(
    path: '/manage-budget-entry',
    name: 'manage',
    builder: (context, state) => AuthenticatedView(
        child: ManageBudgetEntryScreen(
      budgetEntry: state.extra as BudgetEntry?,
    )),
  ),
  GoRoute(
      path: '/login',
      name: 'login',
      builder: (context, state) =>
          const AuthenticatedView(child: ProfileScreen())),
  GoRoute(
    path: '/boardgames',
    name: 'boardgames',
    builder: (context, state) => const BoardGamesScreen(),
  )
]);
