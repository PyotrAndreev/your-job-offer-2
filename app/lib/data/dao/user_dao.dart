import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../../domain/model/user.dart';

class UserDao {
  UserDao();

  Future<User> registerUser(
    User user,
  ) async {
    // var url = 'http://localhost:5000/register';
    //
    // final response = await http.post(
    //   Uri.parse(url),
    //   headers: {
    //     "Content-Type": "application/x-www-form-urlencoded",
    //   },
    //   encoding: Encoding.getByName('utf-8'),
    //   body: {"login": user.login, 'password': user.password},
    // );
    // if (response.statusCode != 200) {
    //   throw Exception('Failed to load data');
    // }

    return User(
        id: "1",
        login: 'admin',
        password: 'qwerty123',
        firstName: 'Иван',
        lastName: 'Иванов',
        middleName: 'Иванович',
        phone: '+79573574583',
        email: 'example@yandex.ru',
        birthDay: '23.09.2037');
  }

  Future<User> loginUser(
    String login,
    String password,
  ) async {
    // var url = 'http://localhost:5000/login';
    //
    // final response = await http.post(
    //   Uri.parse(url),
    //   headers: {
    //     "Content-Type": "application/x-www-form-urlencoded",
    //   },
    //   encoding: Encoding.getByName('utf-8'),
    //   body: {"login": login, 'password': password},
    // );
    // if (response.statusCode != 200) {
    //   throw Exception('Failed to load data');
    // }
    // final user=UserDto.fromJson(response.body.);
    return User(
        id: "1",
        login: 'admin',
        password: 'qwerty123',
        firstName: 'Иван',
        lastName: 'Иванов',
        middleName: 'Иванович',
        phone: '+79573574583',
        email: 'example@yandex.ru',
        birthDay: '23.09.2037');
  }

  Future<User> updateUser(User user) async {
    // var url = 'http://localhost:5000/update';
    //
    // final response = await http.post(
    //   Uri.parse(url),
    //   headers: {
    //     "Content-Type": "application/x-www-form-urlencoded",
    //   },
    //   encoding: Encoding.getByName('utf-8'),
    //   body: {"login": login, 'password': password},
    // );
    // if (response.statusCode != 200) {
    //   throw Exception('Failed to load data');
    // }
    // final user=UserDto.fromJson(response.body.);
    return User(
        id: "1",
        login: 'admin',
        password: 'qwerty123',
        firstName: 'Иван',
        lastName: 'Иванов',
        middleName: 'Иванович',
        phone: '+79573574583',
        email: 'example@yandex.ru',
        birthDay: '23.09.2037'

    );
  }

  Future<User> uploadCV(User user, File file)async {
    // var url = 'http://localhost:5000/upload';
    //
    // final response = await http.post(
    //   Uri.parse(url),
    //   headers: {
    //     "Content-Type": "application/x-www-form-urlencoded",
    //   },
    //   encoding: Encoding.getByName('utf-8'),
    //   body: {"login": user.login, 'password': user.password},
    // );
    // if (response.statusCode != 200) {
    //   throw Exception('Failed to load data');
    // }
    // final user=UserDto.fromJson(response.body.);
    return User(
        id: "1",
        login: 'admin',
        password: 'qwerty123',
        firstName: 'Иван',
        lastName: 'Иванов',
        middleName: 'Иванович',
        phone: '+79573574583',
        email: 'example@yandex.ru',
        birthDay: '23.09.2037'

    );
  }

  Future<void> logout() async {
    setUser(User.getEmptyUser());
  }

  Future<User> getUser() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    String login = prefs.getString('login') ?? '';
    String password = prefs.getString('password') ?? '';
    return User(login: login, password: password);
  }

  Future<bool> setUser(User user) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setString('login', user.login);
    return prefs.setString("password", user.password);
  }
}
