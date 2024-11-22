import 'dart:ui';

import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'localization_provider.g.dart';

@riverpod
class LocalizationState extends _$LocalizationState {
  @override
  Locale build() {
    return const Locale('en');
  }

  void setLocale({required Locale locale}) {
    state = locale;
  }
}
