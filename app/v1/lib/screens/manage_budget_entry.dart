import 'package:amplify_api/amplify_api.dart';
import 'package:amplify_flutter/amplify_flutter.dart';
import 'package:app/models/BudgetEntry.dart';
import 'package:app/widgets/app_bar.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class ManageBudgetEntryScreen extends StatefulWidget {
  const ManageBudgetEntryScreen({
    required this.budgetEntry,
    super.key,
  });

  final BudgetEntry? budgetEntry;

  @override
  State<ManageBudgetEntryScreen> createState() =>
      _ManageBudgetEntryScreenState();
}

class _ManageBudgetEntryScreenState extends State<ManageBudgetEntryScreen> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _titleController = TextEditingController();
  final TextEditingController _descriptionController = TextEditingController();
  final TextEditingController _amountController = TextEditingController();

  late final String _titleText;

  bool get _isCreate => _budgetEntry == null;
  BudgetEntry? get _budgetEntry => widget.budgetEntry;

  @override
  void initState() {
    super.initState();

    final budgetEntry = _budgetEntry;
    if (budgetEntry != null) {
      _titleController.text = budgetEntry.title;
      _descriptionController.text = budgetEntry.description ?? '';
      _amountController.text = budgetEntry.amount.toStringAsFixed(2);
      _titleText = 'Update budget entry';
    } else {
      _titleText = 'Create budget entry';
    }
  }

  @override
  void dispose() {
    _titleController.dispose();
    _descriptionController.dispose();
    _amountController.dispose();
    super.dispose();
  }

  Future<void> submitForm() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    // If the form is valid, submit the data
    final title = _titleController.text;
    final description = _descriptionController.text;
    final amount = double.parse(_amountController.text);

    if (_isCreate) {
      // Create a new budget entry
      final newEntry = BudgetEntry(
        title: title,
        description: description.isNotEmpty ? description : null,
        amount: amount,
      );
      final request = ModelMutations.create(newEntry);
      final response = await Amplify.API.mutate(request: request).response;
      safePrint('Create result: $response');
    } else {
      // Update budgetEntry instead
      final updateBudgetEntry = _budgetEntry!.copyWith(
        title: title,
        description: description.isNotEmpty ? description : null,
        amount: amount,
      );
      final request = ModelMutations.update(updateBudgetEntry);
      final response = await Amplify.API.mutate(request: request).response;
      safePrint('Update result: $response');
    }

    // Navigate back to homepage after create/update executes
    if (mounted) {
      context.pop();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: MyAppBar(title: _titleText),
      body: Align(
        alignment: Alignment.topCenter,
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: SingleChildScrollView(
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    TextFormField(
                      controller: _titleController,
                      decoration: const InputDecoration(
                        labelText: 'Title (required)',
                      ),
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter a title';
                        }
                        return null;
                      },
                    ),
                    TextFormField(
                      controller: _descriptionController,
                      decoration: const InputDecoration(
                        labelText: 'Description',
                      ),
                    ),
                    TextFormField(
                      controller: _amountController,
                      keyboardType: const TextInputType.numberWithOptions(
                        signed: false,
                        decimal: true,
                      ),
                      decoration: const InputDecoration(
                        labelText: 'Amount (required)',
                      ),
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter an amount';
                        }
                        final amount = double.tryParse(value);
                        if (amount == null || amount <= 0) {
                          return 'Please enter a valid amount';
                        }
                        return null;
                      },
                    ),
                    const SizedBox(height: 20),
                    ElevatedButton(
                      onPressed: submitForm,
                      child: Text(_titleText),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
