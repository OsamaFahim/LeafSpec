import 'package:flutter/material.dart';
import 'package:leafspec/constants.dart';

class CustomDialog extends StatelessWidget {
  final String title;
  final String message;
  final IconData icon;
  final String buttonText;
  final VoidCallback onPressed;

  const CustomDialog({
    super.key,
    required this.title,
    required this.message,
    required this.icon,
    required this.buttonText,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(15),
      ),
      elevation: 0,
      backgroundColor: Colors.white,
      child: dialogContent(context),
    );
  }

  Widget dialogContent(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        mainAxisSize:
            MainAxisSize.min, // Ensures the dialog takes only needed space
        children: <Widget>[
          Icon(
            icon,
            size: 40,
            color: Constants.blackColor.withOpacity(.6),
          ),
          SizedBox(height: 16),
          Text(
            title,
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.bold,
              color: Constants.blackColor,
            ),
          ),
          SizedBox(height: 8),
          Text(
            message,
            style: TextStyle(
              fontSize: 16,
              color: Constants.blackColor.withOpacity(.6),
            ),
            textAlign: TextAlign.center,
          ),
          SizedBox(height: 16),
          ElevatedButton(
            onPressed: onPressed,
            style: ElevatedButton.styleFrom(
              backgroundColor: Constants.blackColor.withOpacity(.7),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10),
              ),
            ),
            child: Text(buttonText),
          ),
        ],
      ),
    );
  }
}
