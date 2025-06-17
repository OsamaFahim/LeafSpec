from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import numpy as np
#import tensorflow as tf
import torch
import torch.nn as nn
from torchvision import models, transforms


app = Flask(__name__)

species = [
    "Ailanthus altissima Mill Swingle(182)",
    "Aloe Vera",
    "Alstonia Scholaris",
    "Apple",
    "Arjun",
    "Blueberry",
    "Buxus sempervirens L(200)",
    "Cherry",
    "Corn",
    "Corylus avellana L(199)",
    "Cotinus coggygria Scop(200)",
    "Crataegus monogyna Jacq(200)",
    "Fraxinus angustifolia Vahi(200)",
    "Grape",
    "Guava",
    "Hedera helix L(200)",
    "Jamun",
    "Jatropha",
    "Kale",
    "Laurus nobilis L(200)",
    "Lemon",
    "Mango",
    "Orange",
    "Peach",
    "Pepper Bell",
    "Phillyrea angustifolia L(200)",
    "Pistacia lentiscus L(200)",
    "Pittosporum tobira Thumb WTAiton(200)",
    "Pomegranate",
    "Pongamia Pinnata",
    "Populus alba L(200)",
    "Populus nigra L(200)",
    "Potato",
    "Quercus ilex L(200)",
    "Raspberry",
    "Ruscus aculeatus L(200)",
    "Soybean",
    "Strawberry",
    "Tomato"
]

# MongoDB Atlas connection string
#client = MongoClient("mongodb+srv://admin:admin@leafspeccluster.6emh8.mongodb.net/?retryWrites=true&w=majority&appName=LeafSpecCluster")
#mongodb://localhost:27017/
client = MongoClient("mongodb://localhost:27017/")
# Access the database
db = client['LeafSpec']

@app.route('/')
def home():
    return "Flask is running!"

def user_exists(email):
    user = db.users.find_one({"email": email})
    print(user)
    if (user == None):
        return False
    else:
        return True



# ADD/REGISTER USER
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    print(data)

    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Name, email and password are required"}), 400
    user_exist = user_exists(str(data['email']))
    if(user_exist):
       return jsonify({"error": "User Already exists"}), 409
    
    hashed_password = generate_password_hash(data['password'])

    user_id = db.users.insert_one({
        "name": data['name'],
        "email": data['email'],
        "password": hashed_password

    }).inserted_id

    return jsonify({"user_id": str(user_id)}), 200

# SIGN IN USER
@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    user = db.users.find_one({"email": data['email']})

    if user:
        if check_password_hash(user['password'], data['password']):
            return jsonify({"message": "Login successful", "user_id": str(ObjectId(user['_id']))}), 200
        else:
            return jsonify({"error": "Invalid password"}), 401
    else:
        return jsonify({"error": "User not found"}), 404

#Function to configure and load binary classifier
def load_binary_classifier(model_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = models.resnet18(weights=None)
    model.fc = nn.Sequential(
        nn.Linear(model.fc.in_features, 1),
        nn.Sigmoid()
    )
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()
    return model

#Function to configure and load plant classifier
def load_plant_classifier(model_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = models.resnet34(weights=None)
    model.fc = nn.Linear(model.fc.in_features, len(species))
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()
    return model

# Load the models
binary_classifier_model_path = "../lib/models/Binary_classifier_ResNet18.pth"
binary_classifier_model = load_binary_classifier(binary_classifier_model_path)

# Load plant species classifier
plant_classifier_model_path = "../lib/models/resnet34_plant_classifier.pth"
plant_classifier_model = load_plant_classifier(plant_classifier_model_path)

# PREPROCESS IMAGE
def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    image = image.convert("RGB")
    return transform(image).unsqueeze(0)

# Prediction function
def predict(image_tensor, model):
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        confidence, predicted_idx = torch.max(probabilities, 0)
        predicted_class = species[predicted_idx.item()]
        return predicted_class, confidence.item()

#Validate Image that whether it is specie or not
def Validate(image: Image.Image, binary_classifier_model, plant_classifier_model):
    image_tensor = preprocess_image(image)

    # Step 1: Binary classification
    with torch.no_grad():
        binary_output = binary_classifier_model(image_tensor)
        binary_prob = binary_output.item()  # Already sigmoid applied in model

    # Inverting to get the correct results
    binary_prob = 1 - binary_prob

    # Step 2: Predict species if it's a plant
    if binary_prob >= 0.5:
        predicted_class, confidence = predict(image_tensor, plant_classifier_model)
        return {
            "is_plant": True,
            "binary_confidence": binary_prob,
            "predicted_species": predicted_class,
            "species_confidence": confidence
        }
    else:
        return {
            "is_plant": False,
            "binary_confidence": binary_prob,
            "predicted_species": None,
            "species_confidence": None
        }


# PREDICT SPECIES
@app.route('/predict_species', methods=['POST'])
def predict_species():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    image = Image.open(io.BytesIO(image_file.read())).convert("RGB")

    result = Validate(image, binary_classifier_model, plant_classifier_model)

    # for i, specie in enumerate(species):
    #     print(prediction[0][i])
    if result["is_plant"]:
        return jsonify({
            'is_plant': True,
            'binary_confidence': round(result["binary_confidence"], 4),
            'predicted_species': result["predicted_species"],
            'species_confidence': round(result["species_confidence"], 4)
        })
    else:
        return jsonify({
            'is_plant': False,
            'binary_confidence': round(result["binary_confidence"], 4),
            'message': "The uploaded image is not a plant leaf."
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

