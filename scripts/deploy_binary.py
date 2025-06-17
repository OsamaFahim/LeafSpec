import modelbit
import os
import sys

print("🚀 Deploying Production Binary Classifier...")

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
binary_deployment_dir = os.path.join(project_root, 'binary_deployment')

# Add project root to Python path
sys.path.insert(0, project_root)

# Change to deployment directory
original_cwd = os.getcwd()
os.chdir(binary_deployment_dir)

# Verify deployment files exist
print("Checking deployment files...")
required_files = [
    "binary_classifier.py",
    "requirements.txt", 
    "data/Binary_classifier_ResNet18.pth"
]

for file in required_files:
    if os.path.exists(file):
        if file.endswith('.pth'):
            size = os.path.getsize(file) / (1024*1024)  # Size in MB
            print(f"✅ {file} ({size:.1f} MB)")
        else:
            print(f"✅ {file}")
    else:
        print(f"❌ Missing: {file}")
        exit(1)

try:
    # Import the production binary classifier
    from binary_deployment import binary_classifier
    print("✅ Successfully imported binary_classifier module")
    
    # Deploy to production
    modelbit.deploy(
        binary_classifier.classify_binary,
        name="BinaryClassifier_Production",
        python_version="3.10",
        requirements_txt_path="requirements.txt",
        extra_files=["data/Binary_classifier_ResNet18.pth"]
    )
    
    print("🎉 Production binary classifier deployed successfully!")
    print("📡 API URL: https://nu-edu.us-east-1.aws.modelbit.com/v1/BinaryClassifier_Production/latest")
    
except Exception as e:
    print(f"❌ Deployment failed: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    # Cleanup
    os.chdir(original_cwd)
    if project_root in sys.path:
        sys.path.remove(project_root)

print("🏁 Deployment process completed!")