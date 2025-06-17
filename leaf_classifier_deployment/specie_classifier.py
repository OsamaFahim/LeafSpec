def classify_species(image_bytes: str) -> dict:
    """
    Production species classifier - returns probability vector only
    Cost-efficient approach: do species lookup locally
    """
    
    import torch
    import torch.nn as nn
    import base64
    import io
    from torchvision import models, transforms
    from PIL import Image
    import os
    
    try:
        # Image preprocessing transform
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406],
                               [0.229, 0.224, 0.225])
        ])
        
        # Model path
        model_path = "data/resnet34_plant_classifier.pth"
        
        if not os.path.exists(model_path):
            return {"error": True, "message": "Model not found"}
        
        # Setup device and model (EXACT same as binary classifier)
        device = torch.device("cpu")
        
        # Load ResNet34 model architecture
        model = models.resnet34(pretrained=False)  # Use pretrained=False like binary
        model.fc = nn.Linear(model.fc.in_features, 39)  # 39 species classes
        
        # Load trained weights (EXACT same pattern)
        model.load_state_dict(torch.load(model_path, map_location=device))
        model = model.to(device)
        model.eval()
        
        # Process input image (EXACT same pattern)
        image_data = base64.b64decode(image_bytes)
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        image = transform(image)
        image = image.unsqueeze(0).to(device)
        
        # Make prediction
        with torch.no_grad():
            outputs = model(image)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            
            # Convert to list for JSON serialization
            prob_vector = probabilities.tolist()
        
        # Return only probability vector
        return {
            "probabilities": prob_vector,
            "num_classes": len(prob_vector)
        }
        
    except Exception as e:
        return {
            "error": True,
            "message": "Classification failed"
        }