import 'package:flutter/material.dart';
import 'package:leafspec/constants.dart';

class CustomTextfield extends StatelessWidget {
  final IconData icon;
  final bool obscureText;
  final String hintText;
  final TextEditingController controller;
  final String? Function(String?)? validator;

  const CustomTextfield({
    super.key,
    required this.icon,
    required this.obscureText,
    required this.hintText,
    required this.controller,
    this.validator,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        TextFormField(
          controller: controller,
          obscureText: obscureText,
          style: TextStyle(
            color: Constants.blackColor,
          ),
          decoration: InputDecoration(
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(10),
              borderSide:
                  BorderSide(color: Constants.blackColor.withOpacity(.3)),
            ),
            prefixIcon: Icon(
              icon,
              color: Constants.blackColor.withOpacity(.3),
            ),
            hintText: hintText,
            hintStyle: TextStyle(color: Constants.blackColor.withOpacity(.5)),
            filled: true,
            fillColor: Colors.grey[200],
            errorStyle: TextStyle(color: Colors.red, fontSize: 12),
          ),
          cursorColor: Constants.blackColor.withOpacity(.5),
          validator: validator,
        ),
        const SizedBox(height: 10), // Spacing between fields
      ],
    );
  }
}
