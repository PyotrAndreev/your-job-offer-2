import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:your_job_offer/ui/pages/cv_page.dart';
import 'package:your_job_offer/ui/pages/form_page.dart';
import 'package:your_job_offer/ui/pages/home_page.dart';
import 'package:your_job_offer/ui/pages/login_page.dart';
import 'package:your_job_offer/ui/pages/registration_page.dart';

void main() {
  runApp(
    const ProviderScope(child: MyApp()),
  );
}

class MyApp extends ConsumerWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return MaterialApp(
      title: 'Your job offer',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const HomePage(),
      onGenerateRoute: (settings) {
        final arguments = settings.arguments;
        return MaterialPageRoute(builder: (context) {
          switch (settings.name) {
            case Pages.login:
              return const LoginPage();
            case Pages.registration:
              return const RegistrationPage();
            case Pages.home:
              return const HomePage();
            case Pages.cvUpload:
              return const CVUploadPage();
            case Pages.form:
              if (arguments is FormArguments) {
                return FormPage(arguments);
              } else {
                return const LoginPage();
              }
            default:
              return const LoginPage();
          }
        });
      },
    );
  }
}

class Pages {
  static const String login = '/login';
  static const String registration = '/registration';
  static const String home = '/home';
  static const String form = '/form';
  static const String cvUpload = '/cvUpload';
}
