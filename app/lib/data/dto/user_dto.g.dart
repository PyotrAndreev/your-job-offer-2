// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'user_dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

UserDto _$UserDtoFromJson(Map<String, dynamic> json) => UserDto(
      json['id'] as String? ?? '',
      json['login'] as String? ?? '',
      json['password'] as String? ?? '',
      json['first_name'] as String? ?? '',
      json['last_name'] as String? ?? '',
      json['middle_name'] as String? ?? '',
      json['phone'] as String? ?? '',
      json['email'] as String? ?? '',
      json['birth_day'] as String? ?? '',
    );

Map<String, dynamic> _$UserDtoToJson(UserDto instance) => <String, dynamic>{
      'id': instance.id,
      'login': instance.login,
      'password': instance.password,
      'first_name': instance.firstName,
      'last_name': instance.lastName,
      'middle_name': instance.middleName,
      'phone': instance.phone,
      'email': instance.email,
      'birth_day': instance.birthDay,
    };
