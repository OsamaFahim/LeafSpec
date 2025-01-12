import 'package:flutter/material.dart';
import 'package:leafspec/constants.dart';
import 'package:leafspec/ui/root_page.dart';
import 'package:leafspec/ui/screens/widgets/custom_textfield.dart';
import 'package:leafspec/ui/screens/signin_page.dart';
import 'package:page_transition/page_transition.dart';
import 'package:leafspec/ui/screens/widgets/authentication_validations.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SignUp extends StatefulWidget {
  const SignUp({super.key});

  @override
  _SignUpState createState() => _SignUpState();
}

class _SignUpState extends State<SignUp> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController nameController = TextEditingController();
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();

  Future<void> sendUserData(
      BuildContext context, String name, String email, String password) async {
    var url = Uri.parse('${Constants.ip}/add_user');
    var response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "name": name,
        "email": email,
        "password": password,
      }),
    );

    if (response.statusCode == 200) {
      print('User added successfully');
      Navigator.pushReplacement(
          context,
          PageTransition(
              child: const RootPage(), type: PageTransitionType.bottomToTop));
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('User already exists with same email'),
          backgroundColor: Colors.red,
          action: SnackBarAction(
            label: 'Login',
            onPressed: () {
              Navigator.pushReplacement(
                  context,
                  PageTransition(
                      child: const SignIn(),
                      type: PageTransitionType.bottomToTop));
            },
          ),
        ),
      );
      print('Failed to insert data: ${response.statusCode}');
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
                Image.asset('assets/images/signup.png'),
                const Text(
                  'Sign Up',
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
                  controller: nameController,
                  obscureText: false,
                  hintText: 'Enter Full Name',
                  icon: Icons.person,
                  validator: validateName,
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
                      print('Form is valid');
                      sendUserData(context, nameController.text,
                          emailController.text, passwordController.text);
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
                        'Sign Up',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 18.0,
                        ),
                      ),
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
                            child: const SignIn(),
                            type: PageTransitionType.bottomToTop));
                  },
                  child: Center(
                    child: Text.rich(
                      TextSpan(children: [
                        TextSpan(
                          text: 'Have an Account? ',
                          style: TextStyle(
                            color: Constants.blackColor,
                          ),
                        ),
                        TextSpan(
                          text: 'Login',
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
