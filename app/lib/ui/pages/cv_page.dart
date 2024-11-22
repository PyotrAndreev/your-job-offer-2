import 'dart:io';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:your_job_offer/core/providers.dart';
import 'package:your_job_offer/ui/providers/user/user_provider.dart';

import '../../domain/model/user.dart';
import '../../main.dart';
import 'form_page.dart';

class CVUploadPage extends ConsumerStatefulWidget {
  const CVUploadPage({super.key});

  @override
  ConsumerState<CVUploadPage> createState() => _CVUploadPageState();
}

class _CVUploadPageState extends ConsumerState<CVUploadPage> {
  File? selectedFile;

  Future<void> pickFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf', 'doc', 'docx'],
    );

    if (result != null) {
      setState(() {
        selectedFile = File(result.files.single.path!);
      });
    }
  }

  Future<User?> uploadFile(User user) async {

    if (selectedFile == null) return null;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Файл отправлен: ${selectedFile!.path}')),
    );
    final newUser=await ref.read(userRepositoryProvider).uploadCV(user, selectedFile!);
    if(newUser!=User.getEmptyUser()) {
      ref.read(userStateProvider.notifier).updateUser(newUser);
      return newUser;
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    final user=ref.watch(userStateProvider).valueOrNull ??User.getEmptyUser();
    print('form ${user.login}');
    return Scaffold(
      appBar: AppBar(title: const Text('Загрузка резюме')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: pickFile,
              child: const Text('Выбрать файл'),
            ),
            if (selectedFile != null) Text('Выбран файл: ${selectedFile!.path}'),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () async {
                final upUser =await uploadFile(user);
                if(upUser!=null){
                  if(context.mounted){
                    Navigator.pushNamed(context, Pages.form, arguments: FormArguments(user: upUser));
                  }
                }
              },
              child: const Text('Отправить файл'),
            ),
          ],
        ),
      ),
    );
  }
}
