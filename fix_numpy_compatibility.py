"""
Script to fix NumPy and scikit-learn compatibility issues.
Run this script if you encounter:
- 'ModuleNotFoundError: No module named numpy._core'
- 'No module named _loss'
- Other scikit-learn/numpy compatibility errors
"""

import subprocess
import sys
import os

def fix_environment():
    print("🔧 Fixing NumPy and scikit-learn compatibility issues...")
    print("=" * 60)
    
    # Uninstall conflicting packages
    print("\n1️⃣ Uninstalling potentially conflicting packages...")
    packages_to_uninstall = ["numpy", "scikit-learn", "joblib", "xgboost", "scipy"]
    for pkg in packages_to_uninstall:
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", pkg], 
                         check=False, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✓ Uninstalled {pkg}")
            else:
                print(f"   ℹ {pkg} not installed or already removed")
        except Exception as e:
            print(f"   ⚠ Could not uninstall {pkg}: {e}")
    
    # Install compatible versions in correct order
    print("\n2️⃣ Installing compatible versions (in dependency order)...")
    
    # First install base dependencies
    base_packages = [
        "numpy<2.0.0",
        "scipy>=1.9.0,<1.13.0",  # scipy is a dependency of scikit-learn
    ]
    
    for package in base_packages:
        try:
            print(f"   Installing {package}...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", package], 
                                  check=True, capture_output=True, text=True)
            print(f"   ✓ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}")
            print(f"      Error: {e.stderr[:200]}")
            return False
    
    # Then install scikit-learn and related packages
    ml_packages = [
        "scikit-learn>=1.3.0,<1.5.0",
        "joblib>=1.3.0",
        "xgboost>=1.7.0,<2.1.0"
    ]
    
    for package in ml_packages:
        try:
            print(f"   Installing {package}...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", package], 
                                  check=True, capture_output=True, text=True)
            print(f"   ✓ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}")
            print(f"      Error: {e.stderr[:200]}")
            return False
    
    print("\n3️⃣ Verifying installation...")
    try:
        import numpy
        import sklearn
        import joblib
        import xgboost
        import scipy
        print(f"   ✓ NumPy version: {numpy.__version__}")
        print(f"   ✓ SciPy version: {scipy.__version__}")
        print(f"   ✓ scikit-learn version: {sklearn.__version__}")
        print(f"   ✓ joblib version: {joblib.__version__}")
        print(f"   ✓ xgboost version: {xgboost.__version__}")
        
        # Test importing sklearn modules that use _loss
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.svm import SVC
        print(f"   ✓ Successfully imported scikit-learn models")
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ Environment fixed!")
    print("\n⚠️  IMPORTANT: If model loading still fails, you may need to retrain models.")
    print("   This ensures models are saved with the current scikit-learn version.")
    print("\n   To retrain models, run:")
    print("   python train_and_save_models.py")
    return True

if __name__ == "__main__":
    success = fix_environment()
    if not success:
        print("\n❌ Fix failed. You may need to:")
        print("   1. Check your Python version (3.8+ required)")
        print("   2. Retrain models with current environment")
        print("   3. Manually install: pip install 'numpy<2.0.0' 'scikit-learn>=1.3.0,<1.5.0'")
        sys.exit(1)

