import 'package:flutter/material.dart';
import 'package:leafspec/constants.dart';
import 'package:leafspec/ui/root_page.dart';
import 'package:leafspec/ui/screens/forgot_password.dart';
import 'package:leafspec/ui/screens/signup_page.dart';
import 'package:leafspec/ui/screens/widgets/custom_textfield.dart';
import 'package:page_transition/page_transition.dart';
import 'package:leafspec/ui/screens/widgets/authentication_validations.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SignIn extends StatefulWidget {
  const SignIn({super.key});

  @override
  State<SignIn> createState() => _SignInState();
}

class _SignInState extends State<SignIn> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  final TextEditingController errorController = TextEditingController();

  Future<void> signIn(
      BuildContext context, String email, String password) async {
    var url =
        Uri.parse('${Constants.ip}/sign_in'); // Replace with your backend URL
    var response = await http.post(
      url,
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'email': email,
        'password': password,
      }),
    );

    if (response.statusCode == 200) {
      var data = jsonDecode(response.body);
      print("Login successful! User ID: ${data['user_id']}");
      Navigator.pushReplacement(
          context,
          PageTransition(
              child: const RootPage(), type: PageTransitionType.bottomToTop));
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Password or email is incorrect'),
          backgroundColor: Colors.red,
        ),
      );

      print('Failed to sign in ${response.statusCode}');
    }
  }

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;

    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 20),
        child: SingleChildScrollView(
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Image.asset('assets/images/signin.png'),
                const Text(
                  'Sign In',
                  style: TextStyle(
                    fontSize: 35.0,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: 30),
                CustomTextfield(
                  controller: emailController,
                  obscureText: false,
                  hintText: 'Enter Email',
                  icon: Icons.alternate_email,
                  validator: validateEmail,
                ),
                CustomTextfield(
                  controller: passwordController,
                  obscureText: true,
                  hintText: 'Enter Password',
                  icon: Icons.lock,
                  validator: validatePassword,
                ),
                const SizedBox(height: 10),
                GestureDetector(
                  onTap: () {
                    if (_formKey.currentState!.validate()) {
                      signIn(context, emailController.text,
                          passwordController.text);
                    }
                  },
                  child: Container(
                    width: size.width,
                    decoration: BoxDecoration(
                      color: Constants.primaryColor,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    padding: const EdgeInsets.symmetric(
                        horizontal: 10, vertical: 20),
                    child: const Center(
                      child: Text(
                        'Sign In',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 18.0,
                        ),
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 10),
                GestureDetector(
                  onTap: () {
                    Navigator.pushReplacement(
                        context,
                        PageTransition(
                            child: const ForgotPassword(),
                            type: PageTransitionType.bottomToTop));
                  },
                  child: Center(
                    child: Text.rich(
                      TextSpan(children: [
                        TextSpan(
                          text: 'Forgot Password? ',
                          style: TextStyle(
                            color: Constants.blackColor,
                          ),
                        ),
                        TextSpan(
                          text: 'Reset Here',
                          style: TextStyle(
                            color: Constants.primaryColor,
                          ),
                        ),
                      ]),
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                const Row(
                  children: [
                    Expanded(child: Divider()),
                    Padding(
                      padding: EdgeInsets.symmetric(horizontal: 10),
                      child: Text('OR'),
                    ),
                    Expanded(child: Divider()),
                  ],
                ),
                const SizedBox(height: 20),
                GestureDetector(
                  onTap: () {
                    Navigator.pushReplacement(
                        context,
                        PageTransition(
                            child: const SignUp(),
                            type: PageTransitionType.bottomToTop));
                  },
                  child: Center(
                    child: Text.rich(
                      TextSpan(children: [
                        TextSpan(
                          text: 'New to LeafSpec? ',
                          style: TextStyle(
                            color: Constants.blackColor,
                          ),
                        ),
                        TextSpan(
                          text: 'Register',
                          style: TextStyle(
                            color: Constants.primaryColor,
                          ),
                        ),
                      ]),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
