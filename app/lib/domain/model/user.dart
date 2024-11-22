class User {
  String? id;
  String login;
  String password;
  String? firstName;
  String? lastName;
  String? middleName;
  String? phone;
  String? email;
  String? birthDay;
  String? description;
  int? minSalary;
  int? maxSalary;
  int? workHours;
  String? gender;
  String? workType;
  String? businessTripReadiness;
  String? relocation;
  String? employment;
  String? schedule;

  User({
    this.id,
    required this.login,
    required this.password,
    this.firstName,
    this.lastName,
    this.middleName,
    this.phone,
    this.email,
    this.birthDay,
    this.description,
    this.gender,
    this.maxSalary,
    this.minSalary,
    this.workHours,
    this.businessTripReadiness,
    this.employment,
    this.relocation,
    this.schedule,
    this.workType,
  });

  static User getEmptyUser() {
    return User(login: "", password: "");
  }

  @override
  bool operator ==(Object other) {
    return other is User && other.login == login && other.password == password;
  }
}
