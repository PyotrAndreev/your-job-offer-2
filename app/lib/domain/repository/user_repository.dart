import 'dart:io';

import '../model/user.dart';

abstract interface class UserRepository {
  Future<User> login(String login, String password);

  Future<User> register(User user);

  Future<User> getUserFromLocalStorage();

  Future<void> logout();

  Future<User> updateUser(User user);

  Future<User> uploadCV(User user, File file);
}
