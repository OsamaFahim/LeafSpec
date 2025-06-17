import requests
import base64
import os
import sys

# Species list (local - cost efficient!)
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

# NEW API name
LEAF_CLASSIFIER_URL = "https://nu-edu.us-east-1.aws.modelbit.com/v1/PlantSpeciesDetector_V2/latest"

def test_image(image_path):
    """Test a single image and return species classification result"""
    
    if not os.path.isabs(image_path):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, image_path)
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    try:
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        payload = {"data": image_base64}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(LEAF_CLASSIFIER_URL, json=payload, headers=headers, timeout=20)
        
        if response.status_code == 200:
            result = response.json()
            
            # CORRECT PARSING: Access the "data" key first
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
                        predicted_species = SPECIES_CLASSES[predicted_idx]
                        print(f"{predicted_species} ({max_confidence:.3f})")
                    else:
                        print(f"❌ Invalid class index: {predicted_idx}")
                else:
                    print("❌ No probabilities returned")
                
            else:
                print("❌ API Error")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        test_image(image_path)
    else:
        print("Usage: python test_leaf_classifier_api.py <image_path>")