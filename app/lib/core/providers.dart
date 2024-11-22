import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:your_job_offer/data/dao/user_dao.dart';
import 'package:your_job_offer/data/repository/user_repository_impl.dart';
import 'package:your_job_offer/domain/repository/user_repository.dart';




final userDaoProvider = Provider<UserDao>(
  (ref) => UserDao(),
);

final userRepositoryProvider = Provider<UserRepository>(
  (ref) => UserRepositoryImpl(
    ref.read(userDaoProvider),
  ),
);

