# 🍃 LeafSpec - AI-Powered Plant Species Identification

LeafSpec is an intelligent mobile application that uses deep learning to identify plant species from leaf images. The app employs a two-stage classification system for accurate and efficient plant identification.

##  Features

- **Binary Classification**: First determines if the image contains a leaf
- **Species Identification**: Identifies the specific plant species from 39+ supported species
- **Real-time Processing**: Flask API-powered classification
- **User Management**: Secure user registration and authentication
- **Mobile-Ready**: Cross-platform mobile application
- **Cloud Deployment**: Scalable model deployment using Modelbit

## Architecture

### Two-Stage Classification Pipeline
1. **Binary Classifier** (ResNet18): Determines if image contains a leaf
2. **Species Classifier** (ResNet34): Identifies specific plant species

### Supported Species
- Apple, Mango, Orange, Lemon, Cherry
- Tomato, Potato, Corn, Soybean
- Aloe Vera, Guava, Pomegranate
- And 27+ more species

## 📁 Project Structure

```
LeafSpec/
├── backend/                 # Flask backend API
├── binary_deployment/       # Binary classifier deployment
├── leaf_classifier_deployment/ # Species classifier deployment
├── scripts/                 # Deployment and testing scripts
├── lib/models/             # Trained model files (.pth)
└── mobile_app/             # Mobile application code
```

## 🛠️ Quick Start

### 1. Test the APIs

```bash
# Test binary classification
python scripts/test_binary_api.py sample_leaf.jpg

# Test species classification
python scripts/test_leaf_classifier_api.py sample_leaf.jpg

# Test complete pipeline
python scripts/test_cascade.py sample_leaf.jpg
```

### 2. Run Backend Server

```bash
cd backend
python app.py
```

### 3. Deploy Models (Optional)

```bash
# Deploy binary classifier
python scripts/deploy_binary.py

# Deploy species classifier
python scripts/deploy_leaf_classifier.py
```

## 📊 Model Performance

- **Binary Classifier**: High accuracy in leaf/non-leaf detection
- **Species Classifier**: Trained on 39 plant species
- **Response Time**: < 2 seconds per classification
- **Confidence Scores**: Probability-based predictions

##  API Endpoints

### Binary Classification
```
POST /api/binary-classify
Returns: {"is_plant": boolean, "confidence": float}
```

### Species Classification
```
POST /api/species-classify  
Returns: {"probabilities": [float], "num_classes": int}
```

##  Model Training

If you want to train the models yourself:

1. **Visit Training Repository**: [https://github.com/AhmadRafiq90/Fyp_repo](https://github.com/AhmadRafiq90/Fyp_repo)

2. **For Species Classifier (ResNet34)**:
   - Download `resnet34(leaf_classifier).py`
   - Set your dataset paths
   - Run training script
   - Save model as `resnet34_plant_classifier.pth`

3. **For Binary Classifier (ResNet18)**:
   - Download `resnet18(binary_classifier).py` 
   - Configure leaf/non-leaf dataset paths
   - Train the model
   - Save as `Binary_classifier_ResNet18.pth`

4. **Place trained models** in `lib/models/` directory

## 📱 Technologies Used

- **Backend**: Flask, PyTorch, Torchvision
- **Mobile**: Cross-platform framework
- **Database**: MongoDB
- **Deployment**: Modelbit Cloud APIs
- **Models**: ResNet18 (Binary), ResNet34 (Species)

## 🎯 Usage Example

```python
# Complete classification pipeline
python scripts/test_cascade.py your_leaf_image.jpg

# Expected Output:
# 🔍 Analyzing: your_leaf_image.jpg
# ✅ LEAF detected (confidence: 0.948)
# 🌿 Species: Mango
# 📊 Species confidence: 0.923
```

## 👥 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

**This is the mobile application of our FYP**
