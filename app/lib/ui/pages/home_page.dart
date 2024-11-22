import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'package:uni_links/uni_links.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:your_job_offer/ui/providers/user/user_provider.dart';

import '../../domain/model/user.dart';
import 'login_page.dart';

class HomePage extends ConsumerStatefulWidget {
  const HomePage({super.key});

  @override
  ConsumerState<HomePage> createState() => _HomePageState();
}

class _HomePageState extends ConsumerState<HomePage> {
  final String clientId ='';
  final String clientSecret ='';
  final String redirectUri = "myapp://callback";

  String? accessToken;
  String? refreshToken;

  @override
  void initState() {
    super.initState();
    _handleRedirect();
  }

  void _handleRedirect() async {
    getInitialUri().then((Uri? uri) {
      if (uri != null && uri.toString().startsWith(redirectUri)) {
        final String? code = uri.queryParameters['code'];
        if (code != null) {
          _fetchAccessToken(code);
        }
      }
    });

    uriLinkStream.listen((Uri? uri) {
      if (uri != null && uri.toString().startsWith(redirectUri)) {
        final String? code = uri.queryParameters['code'];
        if (code != null) {
          _fetchAccessToken(code);
        }
      }
    });
  }

  String get authUrl {
    return "https://hh.ru/oauth/authorize?"
        "response_type=code"
        "&client_id=$clientId"
        "&client_secret=$clientSecret"
        "&redirect_uri=${Uri.encodeComponent(redirectUri)}";
  }

  Future<void> _fetchAccessToken(String code) async {
    const String tokenUrl = "https://hh.ru/oauth/token";

    try {
      final response = await http.post(
        Uri.parse(tokenUrl),
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: {
          'grant_type': 'authorization_code',
          'client_id': clientId,
          'client_secret': clientSecret,
          'redirect_uri': redirectUri,
          'code': code,
        },
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> tokenData = json.decode(response.body);
        setState(() {
          accessToken = tokenData['access_token'];
          refreshToken = tokenData['refresh_token'];
        });
        print("Access Token: $accessToken");
        print("Refresh Token: $refreshToken");
      } else {
        print("Ошибка получения токена: ${response.body}");
      }
    } catch (e) {
      print("Произошла ошибка: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    var user = ref.watch(userStateProvider).valueOrNull ?? User.getEmptyUser();
    if (user == User.getEmptyUser()) {
      return const LoginPage();
    } else {
      return Scaffold(
        appBar: AppBar(
          title: const Text('HH.ru Авторизация'),
          actions: [
            IconButton(
              onPressed: () async {
                await ref.read(userStateProvider.notifier).logout();
              },
              icon: Icon(Icons.logout),
            ),
          ],
        ),
        body: Center(
          child: accessToken == null
              ? ElevatedButton(
                  onPressed: () {
                    _launchAuthUrl();
                  },
                  child: const Text('Авторизоваться'),
                )
              : Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text('Успешная авторизация!'),
                    Text('Access Token: $accessToken'),
                    Text('Refresh Token: $refreshToken'),
                  ],
                ),
        ),
      );
    }
  }

  void _launchAuthUrl() async {
    final Uri authUri = Uri.parse(authUrl);
    print(authUri);
    await launchUrl(authUri, mode: LaunchMode.externalApplication);
  }
}
