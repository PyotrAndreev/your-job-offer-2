import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'theme_provider.g.dart';

@riverpod
class ThemeDarkState extends _$ThemeDarkState {
  @override
  bool build() {
    return false;
  }

  void changeTheme() {
    state = !state;
  }
}
