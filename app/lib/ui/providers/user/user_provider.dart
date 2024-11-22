import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:your_job_offer/core/providers.dart';

import '../../../domain/model/user.dart';

part 'user_provider.g.dart';

@riverpod
class UserState extends _$UserState {
  @override
  Future<User> build() async {
    return await ref.read(userRepositoryProvider).getUserFromLocalStorage();
  }

  Future<User> login(String login, String password) async {
    final user = await ref.read(userRepositoryProvider).login(login, password);
    state = AsyncValue.data(user);
    return user;
  }
  Future<User> register(User rawUser) async{
    final user = await ref.read(userRepositoryProvider).register(rawUser);
    state = AsyncValue.data(user);
    return user;
  }
  Future<void> logout()async {
    await ref.read(userRepositoryProvider).logout();
    state = AsyncValue.data(User.getEmptyUser());
  }

  Future<void> updateUser(User user)async {
    state=AsyncValue.data(user);
    print(state.valueOrNull?.login);
  }

}
