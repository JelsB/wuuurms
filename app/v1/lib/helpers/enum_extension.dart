import 'package:app/models/BoardGameType.dart';

extension BoardGameTypeExtension on BoardGameType {
  String get displayValue {
    switch (this) {
      case BoardGameType.CO_OP:
        return 'Co-op';
      case BoardGameType.WORKER_PLACEMENT:
        return 'Worker Placement';
      default:
        return '';
    }
  }
}
