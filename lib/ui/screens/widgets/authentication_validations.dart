String? validateEmail(String? email) {
  print(email);
  if (email == null || email.isEmpty) {
    return 'Email is required';
  }
  // Simple email validation regex
  if (!RegExp(r'^[^@]+@[^@]+\.[^@]+').hasMatch(email)) {
    return 'Enter a valid email';
  }
  return null;
}

String? validatePassword(String? password) {
  print(password);
  if (password == null || password.isEmpty) {
    return 'Password is required';
  }
  if (password.length < 6) {
    return 'Password must be at least 6 characters long';
  }
  return null;
}

String? validateName(String? name) {
  if (name == null || name.isEmpty) {
    return 'Full name is required';
  }
  if (name.length < 3) {
    return 'Name must be at least 3 characters long';
  }
  return null;
}
