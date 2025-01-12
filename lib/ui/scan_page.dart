import 'package:flutter/material.dart';
import 'package:leafspec/constants.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io'; // For working with File objects
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:path/path.dart';

class ScanPage extends StatefulWidget {
  const ScanPage({super.key});

  @override
  State<ScanPage> createState() => _ScanPageState();
}

class _ScanPageState extends State<ScanPage> {
  File? _imageFile;
  final ImagePicker _picker = ImagePicker();
  TextEditingController resultController = TextEditingController();
  TextEditingController confidenceController = TextEditingController();

  // Method to upload image to backend
  Future<void> _uploadImage(File image) async {
    var uri = Uri.parse("${Constants.ip}/predict_species");
    var request = http.MultipartRequest('POST', uri);
    request.files.add(await http.MultipartFile.fromPath('image', image.path,
        filename: basename(image.path)));

    var response = await request.send();

    if (response.statusCode == 200) {
      var responseData = await http.Response.fromStream(response);
      var result = json.decode(responseData.body);
      resultController.text = result['species'].toString();
      confidenceController.text = result['confidence'].toString();
      print("Prediction: ${result['species']}");
    } else {
      print("Failed to upload image: ${response.statusCode}");
    }
  }

  // Method to open camera
  Future<void> _openCamera() async {
    final pickedFile = await _picker.pickImage(source: ImageSource.camera);

    setState(() {
      if (pickedFile != null) {
        setState(() {
          _imageFile = File(pickedFile.path);
        });

        _uploadImage(_imageFile!);
      } else {
        print('No image selected.');
      }
    });
  }

  // Method to open gallery
  Future<void> _openGallery() async {
    final pickedFile = await _picker.pickImage(source: ImageSource.gallery);

    setState(() {
      if (pickedFile != null) {
        setState(() {
          _imageFile = File(pickedFile.path);
        });

        _uploadImage(_imageFile!);
      } else {
        print('No image selected.');
      }
    });
  }

  // Method to show selection options: Camera or Gallery
  void _showImageSourceSelection(BuildContext context) {
    showModalBottomSheet(
        context: context,
        builder: (BuildContext bc) {
          return SafeArea(
            child: Wrap(
              children: <Widget>[
                ListTile(
                  leading: Icon(Icons.camera_alt),
                  title: Text('Camera'),
                  onTap: () {
                    _openCamera();
                    Navigator.of(context).pop();
                  },
                ),
                ListTile(
                  leading: Icon(Icons.photo_library),
                  title: Text('Gallery'),
                  onTap: () {
                    _openGallery();
                    Navigator.of(context).pop();
                  },
                ),
              ],
            ),
          );
        });
  }

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;

    return Scaffold(
      body: Stack(
        children: [
          Positioned(
            top: 50,
            left: 20,
            right: 20,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                GestureDetector(
                  onTap: () {
                    Navigator.pop(context);
                  },
                  child: Container(
                    height: 40,
                    width: 40,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(25),
                      color: Constants.primaryColor.withOpacity(.15),
                    ),
                    child: Icon(
                      Icons.close,
                      color: Constants.primaryColor,
                    ),
                  ),
                ),
                GestureDetector(
                  onTap: () {
                    debugPrint('favorite');
                  },
                  child: Container(
                    height: 40,
                    width: 40,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(25),
                      color: Constants.primaryColor.withOpacity(.15),
                    ),
                    child: IconButton(
                      onPressed: () {},
                      icon: Icon(
                        Icons.share,
                        color: Constants.primaryColor,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
          Positioned(
            top: 100,
            right: 20,
            left: 20,
            child: Container(
              width: size.width * .8,
              height: size.height * .8,
              padding: const EdgeInsets.all(20),
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    GestureDetector(
                      onTap: () {
                        _showImageSourceSelection(context);
                      },
                      child: Column(
                        children: [
                          _imageFile != null
                              ? Container(
                                  height: 200,
                                  width: 200,
                                  decoration: BoxDecoration(
                                    borderRadius: BorderRadius.circular(15),
                                    boxShadow: [
                                      BoxShadow(
                                        color: Colors.black26,
                                        blurRadius: 10,
                                        offset: Offset(0, 4),
                                      ),
                                    ],
                                    border: Border.all(
                                      color: Colors.blueGrey,
                                      width: 2,
                                    ),
                                  ),
                                  child: ClipRRect(
                                    borderRadius: BorderRadius.circular(15),
                                    child: Image.file(
                                      _imageFile!,
                                      fit: BoxFit.cover,
                                    ),
                                  ),
                                )
                              : Image.asset(
                                  'assets/images/code-scan.png',
                                  height: 100,
                                ),
                          const SizedBox(height: 20),
                          Text(
                            'Tap to Scan',
                            style: TextStyle(
                              color: Constants.primaryColor.withOpacity(.80),
                              fontWeight: FontWeight.w500,
                              fontSize: 20,
                            ),
                          ),
                          const SizedBox(height: 20),
                          TextField(
                            enabled: false,
                            controller: resultController,
                            decoration: InputDecoration(
                                labelText: "Result will appear here"),
                            style: TextStyle(
                              color: Constants.primaryColor.withOpacity(.80),
                              fontWeight: FontWeight.w500,
                              fontSize: 20,
                            ),
                          ),
                          TextField(
                            enabled: false,
                            controller: confidenceController,
                            style: TextStyle(
                              color: Constants.primaryColor.withOpacity(.80),
                              fontWeight: FontWeight.w500,
                              fontSize: 20,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
