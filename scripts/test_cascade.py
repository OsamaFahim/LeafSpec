import requests
import base64
import os
import sys

# API URLs
BINARY_URL = "https://nu-edu.us-east-1.aws.modelbit.com/v1/BinaryClassifier_Production/latest"
SPECIES_URL = "https://nu-edu.us-east-1.aws.modelbit.com/v1/PlantSpeciesDetector_V2/latest"

# Species list for local lookup
SPECIES_CLASSES = [
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

def call_binary_api(image_base64):
    """Step 1: Check if image contains a leaf"""
    try:
        payload = {"data": image_base64}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(BINARY_URL, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            
            # Parse response
            if "data" in result:
                prediction = result["data"]
            elif isinstance(result, list) and len(result) > 0:
                prediction = result[0]
            else:
                prediction = result
            
            if isinstance(prediction, dict) and not prediction.get("error"):
                is_plant = prediction.get("is_plant", False)
                confidence = prediction.get("confidence", 0)
                return is_plant, confidence
                
        return None, None
        
    except Exception as e:
        print(f"❌ Binary API Error: {str(e)}")
        return None, None

def call_species_api(image_base64):
    """Step 2: Identify the species"""
    try:
        payload = {"data": image_base64}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(SPECIES_URL, json=payload, headers=headers, timeout=20)
        
        if response.status_code == 200:
            result = response.json()
            
            # Parse response
            if "data" in result:
                prediction = result["data"]
            elif isinstance(result, list) and len(result) > 0:
                prediction = result[0]
            else:
                prediction = result
            
            if isinstance(prediction, dict) and not prediction.get("error"):
                probabilities = prediction.get("probabilities", [])
                
                if probabilities:
                    max_confidence = max(probabilities)
                    predicted_idx = probabilities.index(max_confidence)
                    
                    if predicted_idx < len(SPECIES_CLASSES):
                        species_name = SPECIES_CLASSES[predicted_idx]
                        return species_name, max_confidence
                        
        return None, None
        
    except Exception as e:
        print(f"❌ Species API Error: {str(e)}")
        return None, None

def test_cascade(image_path):
    """Cascade classification: Binary → Species"""
    
    # Make path absolute if relative
    if not os.path.isabs(image_path):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, image_path)
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    print(f"🔍 Analyzing: {os.path.basename(image_path)}")
    print("-" * 50)
    
    try:
        # Load and encode image once
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # STEP 1: Binary Classification
        print("📊 Step 1: Checking if image contains a leaf...")
        is_leaf, binary_confidence = call_binary_api(image_base64)
        
        if is_leaf is None:
            print("❌ Binary classification failed")
            return
        
        if is_leaf:
            print(f"✅ LEAF detected (confidence: {binary_confidence:.3f})")
            
            # STEP 2: Species Classification
            print("📊 Step 2: Identifying species...")
            species_name, species_confidence = call_species_api(image_base64)
            
            if species_name:
                print(f"🌿 Species: {species_name}")
                print(f"📊 Species confidence: {species_confidence:.3f}")
                
                # Final result
                print("\n🎯 FINAL RESULT:")
                print(f"   Type: LEAF")
                print(f"   Species: {species_name}")
                print(f"   Binary confidence: {binary_confidence:.3f}")
                print(f"   Species confidence: {species_confidence:.3f}")
            else:
                print("❌ Species identification failed")
        else:
            print(f"🚫 NOT A LEAF (confidence: {binary_confidence:.3f})")
            print("\n🎯 FINAL RESULT:")
            print(f"   Type: NOT A LEAF")
            print(f"   No species classification needed")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        test_cascade(image_path)
    else:
        print("Usage: python test_cascade.py <image_path>")
        print("Example: python test_cascade.py sample_leaf.jpg")
        print("Example: python test_cascade.py messi.jpeg")