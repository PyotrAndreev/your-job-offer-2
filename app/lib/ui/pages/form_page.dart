import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:your_job_offer/ui/providers/user/user_provider.dart';

import '../../domain/model/user.dart';
import '../../main.dart';

class FormPage extends ConsumerStatefulWidget {
  const FormPage( this.args, {super.key,});
  final FormArguments args;

  @override
  ConsumerState<FormPage> createState() => _FormPageState();
}
class FormArguments {
  final User user ;

  FormArguments({required this.user});
}
class _FormPageState extends ConsumerState<FormPage> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController firstNameController;
  late TextEditingController lastNameController;
  late TextEditingController middleNameController;
  late TextEditingController phoneController;
  late TextEditingController emailController;
  late TextEditingController descriptionController;
  late TextEditingController minSalaryController;
  late TextEditingController maxSalaryController;
  late TextEditingController workHoursController;

  late String gender;
  late String workType;
  late String businessTripReadiness;
  late String relocation;
  late String employment;
  late String schedule;
  late FormArguments args;
  late User user;

  @override
  void initState() {
    super.initState();
    user=widget.args.user;
    print('QQQQ ${user.login}');
    firstNameController = TextEditingController(text: user.firstName);
    lastNameController = TextEditingController(text: user.lastName);
    middleNameController = TextEditingController(text: user.middleName);
    phoneController = TextEditingController(text: user.phone);
    emailController = TextEditingController(text: user.email);
    descriptionController = TextEditingController(text: user.description);
    minSalaryController = TextEditingController(text: user.minSalary.toString());
    maxSalaryController = TextEditingController(text: user.maxSalary.toString());
    workHoursController = TextEditingController(text: user.workHours.toString());

    gender = user.gender ?? 'male';
    workType = user.workType ?? 'office';
    businessTripReadiness = user.businessTripReadiness ?? 'never';
    relocation = user.relocation ?? 'no';
    employment = user.employment ?? 'full';
    schedule = user.schedule ?? 'fullDay';
  }

  Future<void> submitForm() async {
    if (_formKey.currentState!.validate()) {
        user.firstName=firstNameController.text;
        user.lastName=lastNameController.text;
        user.middleName=middleNameController.text;
        user.phone= phoneController.text;
        user.email=emailController.text;
        user.description= descriptionController.text;
        user.minSalary= int.tryParse(minSalaryController.text);
        user.maxSalary =int.tryParse(maxSalaryController.text);
        user.workHours=int.tryParse(workHoursController.text);
        user.gender= gender;
        user.workType=workType;
        user.businessTripReadiness=businessTripReadiness;
        user.relocation= relocation;
        user.employment= employment;
        user.schedule= schedule;

      }

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Форма отправлена')),
      );
    }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Форма пользователя')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              TextFormField(
                controller: firstNameController,
                decoration: const InputDecoration(labelText: 'Имя'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Введите имя';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: lastNameController,
                decoration: const InputDecoration(labelText: 'Фамилия'),
              ),
              TextFormField(
                controller: middleNameController,
                decoration: const InputDecoration(labelText: 'Отчество'),
              ),
              TextFormField(
                controller: phoneController,
                decoration: const InputDecoration(labelText: 'Телефон'),
                keyboardType: TextInputType.phone,
              ),
              TextFormField(
                controller: emailController,
                decoration: const InputDecoration(labelText: 'Email'),
                keyboardType: TextInputType.emailAddress,
                validator: (value) {
                  if (value == null || value.isEmpty || !value.contains('@')) {
                    return 'Введите корректный email';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: descriptionController,
                decoration: const InputDecoration(labelText: 'Описание'),
              ),
              TextFormField(
                controller: minSalaryController,
                decoration: const InputDecoration(labelText: 'Минимальная зарплата'),
                keyboardType: TextInputType.number,
              ),
              TextFormField(
                controller: maxSalaryController,
                decoration: const InputDecoration(labelText: 'Максимальная зарплата'),
                keyboardType: TextInputType.number,
              ),
              TextFormField(
                controller: workHoursController,
                decoration: const InputDecoration(labelText: 'Часы работы'),
                keyboardType: TextInputType.number,
              ),
              DropdownButtonFormField<String>(
                value: gender,
                decoration: const InputDecoration(labelText: 'Пол'),
                items: ['male', 'female']
                    .map((option) => DropdownMenuItem(value: option, child: Text(option)))
                    .toList(),
                onChanged: (value) => setState(() => gender = value!),
              ),
              DropdownButtonFormField<String>(
                value: workType,
                decoration: const InputDecoration(labelText: 'Тип работы'),
                items: ['office', 'remote', 'hybrid', 'field_work']
                    .map((option) => DropdownMenuItem(value: option, child: Text(option)))
                    .toList(),
                onChanged: (value) => setState(() => workType = value!),
              ),
              DropdownButtonFormField<String>(
                value: businessTripReadiness,
                decoration: const InputDecoration(labelText: 'Готовность к командировкам'),
                items: ['ready', 'sometimes', 'never']
                    .map((option) => DropdownMenuItem(value: option, child: Text(option)))
                    .toList(),
                onChanged: (value) => setState(() => businessTripReadiness = value!),
              ),
              DropdownButtonFormField<String>(
                value: relocation,
                decoration: const InputDecoration(labelText: 'Переезд'),
                items: ['no', 'possible', 'desirable']
                    .map((option) => DropdownMenuItem(value: option, child: Text(option)))
                    .toList(),
                onChanged: (value) => setState(() => relocation = value!),
              ),
              DropdownButtonFormField<String>(
                value: employment,
                decoration: const InputDecoration(labelText: 'Занятость'),
                items: ['full', 'part', 'project', 'volunteer', 'probation']
                    .map((option) => DropdownMenuItem(value: option, child: Text(option)))
                    .toList(),
                onChanged: (value) => setState(() => employment = value!),
              ),
              DropdownButtonFormField<String>(
                value: schedule,
                decoration: const InputDecoration(labelText: 'График работы'),
                items: ['fullDay', 'shift', 'flexible', 'remote', 'flyInFlyOut']
                    .map((option) => DropdownMenuItem(value: option, child: Text(option)))
                    .toList(),
                onChanged: (value) => setState(() => schedule = value!),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () async {
                  await submitForm();
                  if(context.mounted){
                    Navigator.pushNamedAndRemoveUntil(context, Pages.home,(route) => false);
                  }
                },
                child: const Text('Отправить'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
