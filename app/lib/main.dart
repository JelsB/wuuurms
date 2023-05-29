import 'package:flutter/material.dart';

import 'app.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await configureAmplify();
  runApp(const MyApp());
}
