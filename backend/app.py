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
import tensorflow as tf



app = Flask(__name__)

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
    

# Load the model
model = tf.keras.models.load_model('../lib/models/best_model.keras')

# PREPROCESS IMAGE
def preprocess_image(image):
    image = image.resize((224, 224))
    image = np.array(image)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# PREDICT SPECIES
@app.route('/predict_species', methods=['POST'])
def predict_species():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    image = Image.open(io.BytesIO(image_file.read()))

    preprocessed_image = preprocess_image(image)
    prediction = model.predict(preprocessed_image)

    species = [
        'Aloe Vera',
        'Alstonia Scholaris',
        'Apple',
        'Arjun',
        'Blueberry',
        'Buxus sempervirens L(200)',
        'Cherry',
        'Corn',
        'Cotinus coggygria Scop(200)',
        'Crataegus monogyna Jacq(200)',
        'Fraxinus angustifolia Vahl(200)',
        'Grape',
        'Guava',
        'Hedera helix L(200)',
        'Jamun',
        'Jatropha',
        'Kale',
        'Laurus nobilis L(200)',
        'Lemon',
        'Mango',
        'Orange',
        'Paddy Rice',
        'Peach',
        'Pepper Bell',
        'Phillyrea angustifolia L(200)',
        'Pistacia lentiscus L(200)',
        'Pittosporum tobira Thunb WTAiton(200)',
        'Pomegranate',
        'Pongamia Pinnata',
        'Populus alba L(200)',
        'Populus nigra L(200)',
        'Potato',
        'Quercus ilex L(200)',
        'Raspberry',
        'Soybean',
        'Spinach',
        'Strawberry',
        'Tobacco',
        'Tomato'
    ]

    # for i, specie in enumerate(species):
    #     print(prediction[0][i])
    predicted_species = species[np.argmax(prediction)]
    confidence = prediction[0][np.argmax(prediction)]
    str_confidence = str(confidence)
    return jsonify({'species': predicted_species , 'confidence': str_confidence})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

