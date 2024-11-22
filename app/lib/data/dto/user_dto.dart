import 'package:json_annotation/json_annotation.dart';

part 'user_dto.g.dart';

@JsonSerializable(explicitToJson: true)
class UserDto {
  @JsonKey(defaultValue: '')
  final String id;
  @JsonKey(defaultValue: '')
  final String login;
  @JsonKey(defaultValue: '')
  final String password;
  @JsonKey(defaultValue: '', name: 'first_name')
  final String firstName;
  @JsonKey(defaultValue: '', name: 'last_name')
  final String lastName;
  @JsonKey(defaultValue: '', name: 'middle_name')
  final String middleName;
  @JsonKey(defaultValue: '')
  final String phone;
  @JsonKey(defaultValue: '')
  final String email;
  @JsonKey(defaultValue: '', name: 'birth_day')
  final String birthDay;

  const UserDto(
      this.id,
      this.login,
      this.password,
      this.firstName,
      this.lastName,
      this.middleName,
      this.phone,
      this.email,
      this.birthDay,
      );

  factory UserDto.fromJson(Map<String, dynamic> json) =>
      _$UserDtoFromJson(json);

  Map<String, dynamic> toJson() => _$UserDtoToJson(this);


}
