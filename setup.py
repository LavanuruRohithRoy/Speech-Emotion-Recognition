#!/usr/bin/env python3
"""
Complete Setup Script for SER Project
Handles dependency installation, project structure, and initial setup
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_header():
    """Print project header"""
    print("🎤 Speech Emotion Recognition (SER) Project Setup")
    print("=" * 60)
    print("This script will set up your SER project completely")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required. Current version:", sys.version)
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_dataset():
    """Check if dataset directory exists"""
    print("🔍 Checking dataset...")
    
    if not os.path.exists("dataset"):
        print("❌ Dataset directory not found!")
        print("Please ensure your RAVDESS dataset is in the 'dataset' folder")
        print("Expected structure: dataset/Actor_01/, dataset/Actor_02/, etc.")
        return False
    
    # Count audio files
    audio_count = 0
    for root, dirs, files in os.walk("dataset"):
        for file in files:
            if file.endswith('.wav'):
                audio_count += 1
    
    if audio_count == 0:
        print("❌ No .wav files found in dataset!")
        return False
    
    print(f"✅ Dataset found with {audio_count} audio files")
    return True

def choose_installation_method():
    """Let user choose between pip and conda installation"""
    print("\n📦 Choose installation method:")
    print("1. pip (Python package manager) - Recommended for most users")
    print("2. conda (Anaconda/Miniconda) - Better for scientific packages on Windows")
    
    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice == "1":
            return "pip"
        elif choice == "2":
            return "conda"
        else:
            print("Please enter 1 or 2")

def install_dependencies(method):
    """Install project dependencies using chosen method"""
    print(f"📦 Installing dependencies using {method}...")
    
    try:
        if method == "pip":
            # Run the pip dependency installation script
            result = subprocess.run([sys.executable, "install_dependencies.py"], 
                                  capture_output=True, text=True, check=True)
        else:  # conda
            # Run the conda dependency installation script
            result = subprocess.run([sys.executable, "install_conda.py"], 
                                  capture_output=True, text=True, check=True)
        
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Dependency installation failed: {e}")
        print("Error output:", e.stderr)
        
        if method == "pip":
            print("\n💡 Try the conda method instead:")
            print("python install_conda.py")
        else:
            print("\n💡 Try the pip method instead:")
            print("python install_dependencies.py")
        
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating project directories...")
    
    directories = [
        "temp",
        "uploads",
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created {directory}/")
    
    return True

def test_application():
    """Test if the application can start"""
    print("🧪 Testing application...")
    
    try:
        # Try to import the app
        import app
        print("✅ Application imports successfully")
        return True
    except Exception as e:
        print(f"❌ Application test failed: {e}")
        return False

def run_training():
    """Run the model training"""
    print("🚀 Starting model training...")
    print("⚠️  This will take several minutes depending on your dataset size.")
    
    response = input("Do you want to proceed with training? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("⏭️  Skipping training. You can run it later with: python train_model.py")
        return True
    
    try:
        # Run training
        result = subprocess.run([sys.executable, "train_model.py"], 
                              capture_output=True, text=True, check=True)
        print("✅ Training completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Training failed: {e}")
        print("Error output:", e.stderr)
        return False

def create_startup_script():
    """Create a simple startup script"""
    print("📝 Creating startup script...")
    
    startup_content = """@echo off
echo Starting SER Application...
python app.py
pause
"""
    
    with open("start_ser.bat", "w") as f:
        f.write(startup_content)
    
    print("✅ Created start_ser.bat (Windows)")
    
    # Also create a Python startup script
    python_startup = """#!/usr/bin/env python3
import subprocess
import sys

print("Starting SER Application...")
try:
    subprocess.run([sys.executable, "app.py"])
except KeyboardInterrupt:
    print("\\nApplication stopped by user")
"""
    
    with open("start_ser.py", "w") as f:
        f.write(python_startup)
    
    print("✅ Created start_ser.py (Cross-platform)")

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check dataset
    if not check_dataset():
        return False
    
    # Create directories
    if not create_directories():
        return False
    
    # Choose installation method
    method = choose_installation_method()
    
    # Install dependencies
    if not install_dependencies(method):
        return False
    
    # Test application
    if not test_application():
        return False
    
    # Create startup scripts
    create_startup_script()
    
    # Ask about training
    if not run_training():
        print("⚠️  Training failed, but you can try again later")
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    print("\n📋 Next steps:")
    print("1. If training was successful, run: python app.py")
    print("2. If training was skipped, run: python train_model.py first")
    print("3. Open your browser and go to: http://localhost:5000")
    
    print("\n🚀 Quick start options:")
    print("- Windows: Double-click start_ser.bat")
    print("- Any OS: python start_ser.py")
    print("- Manual: python app.py")
    
    print("\n📁 Project structure:")
    print("- src/features/ - Audio feature extraction")
    print("- src/models/ - Model training and management")
    print("- src/utils/ - Helper functions")
    print("- src/templates/ - Web interface templates")
    print("- src/static/ - Static files (CSS, JS, audio)")
    
    print("\n💡 Tips:")
    print("- Keep your dataset in the 'dataset' folder")
    print("- Model files are saved in the root directory")
    print("- Check logs/ for any error messages")
    print("- Use feedback.html to improve the model")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎊 Your SER project is ready to use!")
        else:
            print("\n❌ Setup failed. Please check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)
