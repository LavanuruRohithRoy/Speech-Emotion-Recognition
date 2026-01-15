#!/usr/bin/env python3
"""
Dependency Installation Script for SER Project
Installs compatible versions of required packages with Windows-specific handling
"""

import subprocess
import sys
import os
import platform

def install_package(package):
    """Install a single package with error handling"""
    try:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def check_package(package_name):
    """Check if a package is already installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def install_windows_dependencies():
    """Install Windows-specific dependencies first"""
    print("🪟 Installing Windows-specific dependencies...")
    
    # Install Visual C++ build tools if needed
    try:
        import setuptools
        print("✅ setuptools available")
    except ImportError:
        print("Installing setuptools...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools"])
    
    # Install wheel for better binary package handling
    try:
        import wheel
        print("✅ wheel available")
    except ImportError:
        print("Installing wheel...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "wheel"])

def main():
    """Main installation function"""
    print("🔧 Installing SER Project Dependencies")
    print("=" * 50)
    
    # Check if we're on Windows
    is_windows = platform.system() == "Windows"
    if is_windows:
        print("🪟 Windows detected - installing Windows-specific dependencies first")
        install_windows_dependencies()
    
    # List of packages with compatible versions (order matters!)
    packages = [
        "numpy==1.21.6",           # Install numpy first
        "scipy==1.7.3",            # Then scipy
        "pandas==1.3.5",           # Then pandas
        "scikit-learn==1.0.2",     # Then scikit-learn
        "matplotlib==3.5.2",       # Then matplotlib
        "seaborn==0.11.2",         # Then seaborn
        "Flask==2.2.5",
        "librosa==0.10.1",
        "soundfile==0.12.1",
        "pydub==0.25.1",
        "SpeechRecognition==3.10.0",
        "joblib==1.1.1"
    ]
    
    # Check if pip is available
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
    except subprocess.CalledProcessError:
        print("❌ pip not available. Please install pip first.")
        return False
    
    # Update pip first
    print("📦 Updating pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ pip updated successfully")
    except subprocess.CalledProcessError:
        print("⚠️  Failed to update pip, continuing...")
    
    print("📦 Starting package installation...")
    
    failed_packages = []
    successful_packages = []
    
    for package in packages:
        package_name = package.split("==")[0]
        
        # Check if already installed
        if check_package(package_name):
            print(f"ℹ️  {package_name} already installed, skipping...")
            successful_packages.append(package_name)
            continue
        
        # Install package
        if install_package(package):
            successful_packages.append(package_name)
        else:
            failed_packages.append(package)
            
            # Special handling for problematic packages
            if package_name in ["scikit-learn", "matplotlib"]:
                print(f"\n💡 Special handling for {package_name}:")
                if is_windows:
                    print("   - Try installing Visual C++ build tools")
                    print("   - Or use pre-compiled wheels")
                    print("   - Consider using conda instead of pip")
                
                # Try alternative installation method
                try:
                    print(f"   - Trying alternative installation for {package_name}...")
                    if package_name == "scikit-learn":
                        alt_package = "scikit-learn"
                    elif package_name == "matplotlib":
                        alt_package = "matplotlib"
                    else:
                        alt_package = package
                    
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "--only-binary=:all:", alt_package])
                    print(f"✅ {package_name} installed with alternative method!")
                    successful_packages.append(package_name)
                    failed_packages.remove(package)
                except:
                    print(f"   - Alternative installation failed for {package_name}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Installation Summary")
    print("=" * 50)
    
    print(f"✅ Successfully installed: {len(successful_packages)} packages")
    print(f"❌ Failed to install: {len(failed_packages)} packages")
    
    if successful_packages:
        print(f"\n✅ Installed packages: {', '.join(successful_packages)}")
    
    if failed_packages:
        print(f"\n❌ Failed packages: {', '.join(failed_packages)}")
        print("\n💡 Troubleshooting tips:")
        
        if is_windows:
            print("🪟 Windows-specific solutions:")
            print("1. Install Visual C++ build tools:")
            print("   - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/")
            print("   - Install 'C++ build tools' workload")
            print("2. Try using conda instead of pip:")
            print("   - Install Miniconda: https://docs.conda.io/en/latest/miniconda.html")
            print("   - Run: conda install scikit-learn matplotlib")
            print("3. Use pre-compiled wheels:")
            print("   - Run: pip install --only-binary=:all: scikit-learn matplotlib")
        
        print("\n🔧 General solutions:")
        print("1. Try updating pip: python -m pip install --upgrade pip")
        print("2. Install system audio libraries (Linux)")
        print("3. Check internet connection")
        print("4. Try installing packages one by one")
    
    if not failed_packages:
        print("\n🎉 All dependencies installed successfully!")
        print("You can now run: python train_model.py")
        return True
    else:
        print(f"\n⚠️  Some packages failed to install. Please fix the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
