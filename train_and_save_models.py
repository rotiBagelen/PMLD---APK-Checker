# train_and_save_models.py
import pandas as pd
import joblib
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# --- KONFIGURASI ---
# Ganti dengan path ke dataset CSV Anda
DATASET_PATH = "data.csv" # Pastikan file ini ada di folder D:\apktrust
TARGET_COLUMN = "Result" # Ganti dengan nama kolom target/label Anda

print("Memulai proses pelatihan dan penyimpanan model...")

# 1. Muat Dataset
try:
    df = pd.read_csv(DATASET_PATH)
except FileNotFoundError:
    print(f"❌ Error: File dataset '{DATASET_PATH}' tidak ditemukan!")
    exit()

print(f"✅ Dataset dimuat. Jumlah baris: {len(df)}")

# 2. Pra-pemrosesan Sederhana
# Mengubah semua kolom fitur menjadi numerik (0 atau 1)
X = df.drop(columns=[TARGET_COLUMN])
y = df[TARGET_COLUMN]

# Pastikan semua kolom fitur adalah numerik
X = X.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

# Simpan daftar kolom fitur
feature_columns = X.columns.tolist()
joblib.dump(feature_columns, 'feature_columns.joblib')
print("✅ Daftar kolom fitur disimpan ke 'feature_columns.joblib'")

# Encode label target jika berupa string (misalnya, 'benign', 'malicious')
if y.dtype == 'object':
    le = LabelEncoder()
    y = le.fit_transform(y) # benign=0, malicious=1

# 3. Bagi Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print("✅ Data dibagi menjadi data latih dan uji.")

# 4. Inisialisasi Model
models = {
    "RandomForest": RandomForestClassifier(random_state=42),
    "SVM": SVC(probability=True, random_state=42),
    "GradientBoosting": GradientBoostingClassifier(random_state=42),
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
}

model_accuracies = {}

# 5. Latih, Evaluasi, dan Simpan Setiap Model
for name, model in models.items():
    print(f"\n--- Melatih model: {name} ---")
    model.fit(X_train, y_train)
    
    # Evaluasi akurasi
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    model_accuracies[name] = accuracy
    print(f"🎯 Akurasi {name}: {accuracy:.4f}")
    
    # Simpan model yang sudah dilatih
    model_filename = f"{name.lower()}_model.joblib"
    joblib.dump(model, model_filename)
    print(f"💾 Model disimpan ke '{model_filename}'")

# 6. Simpan Akurasi
with open('model_accuracies.json', 'w') as f:
    json.dump(model_accuracies, f, indent=4)
print("\n✅ Akurasi model disimpan ke 'model_accuracies.json'")

print("\n🎉 Proses Selesai! Semua model dan file yang diperlukan telah dibuat.")