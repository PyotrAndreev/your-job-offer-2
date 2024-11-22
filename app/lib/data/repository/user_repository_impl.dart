import 'dart:io';

import 'package:your_job_offer/domain/model/user.dart';

import '../../domain/repository/user_repository.dart';
import '../dao/user_dao.dart';

class UserRepositoryImpl implements UserRepository {
  final UserDao userDao;

  UserRepositoryImpl(this.userDao,);

  @override
  Future<User> getUserFromLocalStorage() async {
    User user = await userDao.getUser();
    return user;
  }

  @override
  Future<User> login(String login, String password) async {
    User user = await userDao.loginUser(login, password);
    await userDao.setUser(user);
    return user;
  }

  @override
  Future<void> logout() async {
    await userDao.logout();
  }


  @override
  Future<User> register(User user) async {
    User newUser = await userDao.registerUser(user);
    return newUser;
  }

  @override
  Future<User> updateUser(User user) async {
    final updatedUser= await userDao.updateUser(user);
    return updatedUser;
  }

  @override
  Future<User> uploadCV(User user, File file) async {
    final updatedUser= await userDao.uploadCV(user,file);
    return updatedUser;
  }


}