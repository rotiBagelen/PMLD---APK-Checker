"""
Diagnostic script to identify permission name mismatches between
training data and extracted permissions from androguard.
"""

import pandas as pd
import joblib
import json
import os

def normalize_permission_name(perm):
    """Normalize permission names to handle different formats"""
    if not perm:
        return ""
    # Remove common prefixes
    perm = perm.strip()
    if perm.startswith("android.permission."):
        perm = perm.replace("android.permission.", "")
    elif perm.startswith("com.android."):
        perm = perm.replace("com.android.", "")
    return perm.upper()

def load_feature_columns():
    """Load feature columns from saved model"""
    try:
        feature_columns = joblib.load("feature_columns.joblib")
        return feature_columns
    except FileNotFoundError:
        print("❌ feature_columns.joblib not found!")
        return None

def check_training_data_format():
    """Check the format of permissions in training CSV"""
    try:
        df = pd.read_csv("data.csv")
        feature_cols = [col for col in df.columns if col != "Result"]
        print(f"✅ Training data loaded. Found {len(feature_cols)} feature columns.")
        print("\nSample feature column names (first 10):")
        for col in feature_cols[:10]:
            print(f"  - {col}")
        return feature_cols
    except FileNotFoundError:
        print("❌ data.csv not found!")
        return None

def check_extracted_permissions_format():
    """Check format of permissions from androguard (simulated)"""
    # Sample permissions that androguard typically returns
    sample_androguard_perms = [
        "android.permission.INTERNET",
        "android.permission.ACCESS_NETWORK_STATE",
        "android.permission.WRITE_EXTERNAL_STORAGE",
        "com.google.android.gms.permission.AD_ID",
    ]
    print("\n📱 Sample permissions from androguard (typical format):")
    for perm in sample_androguard_perms:
        print(f"  - {perm}")
    return sample_androguard_perms

def diagnose_mismatch():
    """Main diagnostic function"""
    print("=" * 70)
    print("🔍 DIAGNOSING PERMISSION NAME MISMATCH")
    print("=" * 70)
    
    # 1. Check feature columns from model
    print("\n1️⃣ Loading feature columns from trained model...")
    feature_columns = load_feature_columns()
    if not feature_columns:
        return
    
    # 2. Check training data format
    print("\n2️⃣ Checking training data format...")
    training_cols = check_training_data_format()
    if not training_cols:
        return
    
    # 3. Check androguard format
    print("\n3️⃣ Expected androguard permission format...")
    androguard_sample = check_extracted_permissions_format()
    
    # 4. Compare formats
    print("\n4️⃣ Analyzing format differences...")
    
    # Check if training uses full names or short names
    training_has_prefix = any(col.startswith("android.permission.") for col in training_cols[:10])
    training_uppercase = all(col.isupper() or col.replace("_", "").isupper() for col in training_cols[:10] if not training_has_prefix)
    
    print(f"\n📊 Training data format analysis:")
    print(f"  - Uses 'android.permission.' prefix: {training_has_prefix}")
    print(f"  - Uses uppercase/short names: {training_uppercase}")
    
    # 5. Show mismatch
    print("\n5️⃣ Mismatch Analysis:")
    print("=" * 70)
    
    if not training_has_prefix:
        print("⚠️  MISMATCH DETECTED!")
        print("\nThe training data uses SHORT permission names (e.g., 'INTERNET'),")
        print("but androguard returns FULL permission names (e.g., 'android.permission.INTERNET').")
        print("\n✅ SOLUTION: Normalize permission names during feature extraction.")
        print("\nThis can be fixed by updating the run_ml_predictions function to:")
        print("  1. Strip 'android.permission.' prefix from extracted permissions")
        print("  2. Convert to uppercase")
        print("  3. Match against feature columns")
    else:
        print("✅ Format appears compatible (both use full permission names).")
        print("If still having issues, check for case sensitivity or other differences.")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    diagnose_mismatch()

