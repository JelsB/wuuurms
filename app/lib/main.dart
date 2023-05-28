import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'models/ModelProvider.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await _configureAmplify();
  runApp(const MyApp());
}

Future<void> _configureAmplify() async {
  // To be filled in
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // GoRouter configuration
  static final _router = GoRouter(
    routes: [
      GoRoute(
        path: '/',
        builder: (context, state) => const HomeScreen(),
      ),
    ],
  );

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: _router,
      debugShowCheckedModeBanner: false,
    );
  }
}

class LoadingScreen extends StatelessWidget {
  const LoadingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: CircularProgressIndicator(),
      ),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  var _budgetEntries = <BudgetEntry>[];

  @override
  void initState() {
    super.initState();
  }

  Future<void> _refreshBudgetEntries() async {
    // To be filled in
  }

  Future<void> _deleteBudgetEntry(BudgetEntry budgetEntry) async {
    // To be filled in
  }

  Future<void> _navigateToBudgetEntry({BudgetEntry? budgetEntry}) async {
    // To be filled in
  }

  double _calculateTotalBudget(List<BudgetEntry?> items) {
    var totalAmount = 0.0;
    for (final item in items) {
      totalAmount += item?.amount ?? 0;
    }
    return totalAmount;
  }

  Widget _buildRow({
    required String title,
    required String description,
    required String amount,
    TextStyle? style,
  }) {
    return Row(
      children: [
        Expanded(
          child: Text(
            title,
            textAlign: TextAlign.center,
            style: style,
          ),
        ),
        Expanded(
          child: Text(
            description,
            textAlign: TextAlign.center,
            style: style,
          ),
        ),
        Expanded(
          child: Text(
            amount,
            textAlign: TextAlign.center,
            style: style,
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      floatingActionButton: FloatingActionButton(
        // Navigate to the page to create new budget entries
        onPressed: _navigateToBudgetEntry,
        child: const Icon(Icons.add),
      ),
      appBar: AppBar(
        title: const Text('Budget Tracker'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.only(top: 25),
          child: RefreshIndicator(
            onRefresh: _refreshBudgetEntries,
            child: Column(
              children: [
                if (_budgetEntries.isEmpty)
                  const Text('Use the \u002b sign to add new budget entries')
                else
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      // Show total budget from the list of all BudgetEntries
                      Text(
                        'Total Budget: \$ ${_calculateTotalBudget(_budgetEntries).toStringAsFixed(2)}',
                        style: const TextStyle(fontSize: 24),
                      )
                    ],
                  ),
                const SizedBox(height: 30),
                _buildRow(
                  title: 'Title',
                  description: 'Description',
                  amount: 'Amount',
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                const Divider(),
                Expanded(
                  child: ListView.builder(
                    itemCount: _budgetEntries.length,
                    itemBuilder: (context, index) {
                      final budgetEntry = _budgetEntries[index];
                      return Dismissible(
                        key: ValueKey(budgetEntry),
                        background: const ColoredBox(
                          color: Colors.red,
                          child: Padding(
                            padding: EdgeInsets.only(right: 10),
                            child: Align(
                              alignment: Alignment.centerRight,
                              child: Icon(Icons.delete, color: Colors.white),
                            ),
                          ),
                        ),
                        onDismissed: (_) => _deleteBudgetEntry(budgetEntry),
                        child: ListTile(
                          onTap: () => _navigateToBudgetEntry(
                            budgetEntry: budgetEntry,
                          ),
                          title: _buildRow(
                            title: budgetEntry.title,
                            description: budgetEntry.description ?? '',
                            amount:
                                '\$ ${budgetEntry.amount.toStringAsFixed(2)}',
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
