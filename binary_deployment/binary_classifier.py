def classify_binary(image_bytes: str) -> dict:
    """
    Production binary classifier for leaf detection
    Returns clean prediction without debug information
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
        model_path = "data/Binary_classifier_ResNet18.pth"
        
        if not os.path.exists(model_path):
            return {"error": True, "message": "Model not found"}
        
        # Setup device and model
        device = torch.device("cpu")
        
        # Load ResNet18 model architecture
        model = models.resnet18(pretrained=False)  
        model.fc = nn.Sequential(
            nn.Linear(model.fc.in_features, 1),
            nn.Sigmoid()
        )
        
        # Load trained weights
        model.load_state_dict(torch.load(model_path, map_location=device))
        model = model.to(device)
        model.eval()
        
        # Process input image
        image_data = base64.b64decode(image_bytes)
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        image = transform(image)
        image = image.unsqueeze(0).to(device)
        
        # Make prediction
        with torch.no_grad():
            output = model(image)
            raw_prob = output.item()
            
            # Apply probability correction (model outputs inverse probability)
            leaf_probability = 1 - raw_prob
            
            # Determine if image contains a leaf
            is_leaf = leaf_probability >= 0.5
        
        # Return clean production result
        return {
            "is_plant": is_leaf,
            "confidence": round(leaf_probability, 4)
        }
        
    except Exception as e:
        return {
            "error": True,
            "message": "Classification failed"
        }