import requests
import base64
import os
import sys

# Update this URL to your production deployment
BINARY_URL = "https://nu-edu.us-east-1.aws.modelbit.com/v1/BinaryClassifier_Production/latest"

def test_image(image_path):
    """Test a single image and return leaf/no leaf result"""
    
    # Make path absolute if relative
    if not os.path.isabs(image_path):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, image_path)
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    try:
        # Load and encode image
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Send to API
        payload = {"data": image_base64}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(BINARY_URL, json=payload, headers=headers, timeout=15)
        
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
                is_plant = prediction.get("is_plant", False)
                confidence = prediction.get("confidence", 0)
                
                result_text = "LEAF" if is_plant else "NO LEAF"
                print(f"{result_text} ({confidence:.3f})")
                
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
        print("Usage: python test_binary_api.py <image_path>")
        print("Example: python test_binary_api.py messi.jpeg")