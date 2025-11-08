"""
Flask REST API Backend for APKTrust
Replaces Streamlit with REST API for frontend integration
"""

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import sys
import json
import subprocess
import tempfile
import threading
import time
import requests
import joblib
import pandas as pd
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
from hashlib import sha1

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder="./FRONTEND PMLD REVISED/AUTOPENTEST/dist", static_url_path="")
# Enable CORS for frontend - allow all origins for external access
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FILES_DIR = os.path.join(BASE_DIR, "output_files")
ALLOWED_EXTENSIONS = {'apk'}

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FILES_DIR, exist_ok=True)

# Configuration
API_KEY = os.getenv("API_KEY")
MOBSF_URL = os.getenv("MOBSF_URL", "http://host.docker.internal:8000")
PYTHON_VENV_PATH = sys.executable
MODEL_NAMES = ["RandomForest", "SVM", "GradientBoosting", "XGBoost"]
REPORT_PATH = os.path.join(OUTPUT_FILES_DIR, "mobsf_report.json")

# Store analysis results in memory (in production, use Redis or database)
analysis_results = {}
analyzed_apk = {}

# Load ML models once at startup
print("Loading ML models...")
try:
    ml_models = {}
    feature_columns = None
    model_accuracies = {}
    
    for name in MODEL_NAMES:
        model_path = os.path.join(BASE_DIR, f"{name.lower()}_model.joblib")
        if os.path.exists(model_path):
            ml_models[name] = joblib.load(model_path)
            print(f"✓ Loaded {name} model")
    
    if os.path.exists(os.path.join(BASE_DIR, "feature_columns.joblib")):
        feature_columns = joblib.load(os.path.join(BASE_DIR, "feature_columns.joblib"))
        print(f"✓ Loaded {len(feature_columns)} feature columns")
    
    if os.path.exists(os.path.join(BASE_DIR, "model_accuracies.json")):
        with open(os.path.join(BASE_DIR, "model_accuracies.json"), 'r') as f:
            model_accuracies = json.load(f)
        print("✓ Loaded model accuracies")
    
    print("✅ All ML assets loaded successfully")
except Exception as e:
    print(f"❌ Error loading ML models: {e}")
    ml_models = {}
    feature_columns = []
    model_accuracies = {}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def normalize_permission_for_matching(permission):
    """Normalize permission names to match training data format"""
    if not permission:
        return ""
    normalized = permission.strip()
    if normalized.startswith("android.permission."):
        normalized = normalized.replace("android.permission.", "")
    elif normalized.startswith("com.android."):
        normalized = normalized.replace("com.android.", "")
    normalized = normalized.upper()
    return normalized


def extract_permissions_via_subprocess(apk_path):
    """Extract permissions from APK using androguard"""
    try:
        script_path = os.path.join(BASE_DIR, "extract_permissions.py")
        result = subprocess.run(
            [PYTHON_VENV_PATH, script_path, apk_path],
            capture_output=True,
            text=True,
            check=False,
            encoding='utf-8'
        )
        
        if result.returncode != 0:
            return set()
        
        stdout = result.stdout.strip()
        if not stdout:
            return set()
        
        json_start = stdout.find('{')
        if json_start == -1:
            return set()
        
        json_str = stdout[json_start:]
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            brace_count = 0
            json_end = -1
            for i, char in enumerate(json_str):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        json_end = i + 1
                        break
            if json_end > 0:
                data = json.loads(json_str[:json_end])
            else:
                return set()
        
        if "error" in data:
            return set()
        
        return set(data.get("permissions", []))
    except Exception as e:
        print(f"Error extracting permissions: {e}")
        return set()


def run_ml_predictions(permissions_set, models, feature_columns, accuracies):
    """Run ML predictions on extracted permissions"""
    if not models or not feature_columns:
        return []
    
    normalized_perms = {normalize_permission_for_matching(perm): perm for perm in permissions_set}
    normalized_perms_set = set(normalized_perms.keys())
    
    matched_features_original = sum(1 for col in feature_columns if col in permissions_set)
    matched_features_normalized = sum(1 for col in feature_columns if normalize_permission_for_matching(col) in normalized_perms_set or col in normalized_perms_set)
    
    use_normalized = matched_features_normalized > matched_features_original
    
    row = {}
    for col in feature_columns:
        col_normalized = normalize_permission_for_matching(col)
        if use_normalized:
            if col in normalized_perms_set or col_normalized in normalized_perms_set or col.upper() in normalized_perms_set:
                row[col] = 1
            else:
                row[col] = 0
        else:
            row[col] = 1 if col in permissions_set else 0
    
    prediction_df = pd.DataFrame([row], columns=feature_columns)
    
    results = []
    for name, model in models.items():
        confidence = model.predict_proba(prediction_df)[0][1]
        
        # 3-tier prediction system based on confidence threshold
        # < 30%: Aman (Benign)
        # 30% - 50%: Perhatian (Warning)
        # >= 50%: Berbahaya (Dangerous)
        if confidence < 0.30:
            pred_text = "Aman"
            pred_category = "safe"
        elif confidence < 0.50:
            pred_text = "Perhatian"
            pred_category = "warning"
        else:
            pred_text = "Berbahaya"
            pred_category = "dangerous"
        
        results.append({
            "model": name,
            "prediction": pred_text,
            "category": pred_category,
            "confidence": float(confidence),
            "accuracy": float(accuracies.get(name, 0))
        })
    
    return results


def upload_file_to_mobsf(file_name, file_bytes):
    """Upload APK file to MobSF"""
    from requests_toolbelt.multipart.encoder import MultipartEncoder
    
    if not API_KEY:
        raise ValueError("API_KEY is not configured")
    
    mp_encoder = MultipartEncoder(fields={'file': (file_name, file_bytes, 'application/octet-stream')})
    headers = {'Authorization': API_KEY, 'Content-Type': mp_encoder.content_type}
    response = requests.post(f"{MOBSF_URL}/api/v1/upload", data=mp_encoder, headers=headers, timeout=300)
    
    if response.status_code == 401:
        raise ValueError("401 Unauthorized - Invalid API key")
    response.raise_for_status()
    return response.json()


def start_scan(upload_data):
    """Start MobSF scan"""
    if not API_KEY:
        raise ValueError("API_KEY is not configured")
    response = requests.post(f"{MOBSF_URL}/api/v1/scan", data={"hash": upload_data['hash']}, headers={'Authorization': API_KEY}, timeout=300)
    if response.status_code == 401:
        raise ValueError("401 Unauthorized")
    response.raise_for_status()
    return response.json()


def generate_json_report(hash_value):
    """Generate MobSF JSON report"""
    if not API_KEY:
        raise ValueError("API_KEY is not configured")
    time.sleep(90)  # Wait for scan to complete
    response = requests.post(f"{MOBSF_URL}/api/v1/report_json", data={'hash': hash_value}, headers={'Authorization': API_KEY}, timeout=300)
    if response.status_code == 401:
        raise ValueError("401 Unauthorized")
    response.raise_for_status()
    return response.json()


def parse_summary(raw_output: str) -> str:
    """Parse LLM summary output"""
    keyword = "executive summary:"
    lower_output = raw_output.lower()
    keyword_pos = lower_output.rfind(keyword)
    if keyword_pos != -1:
        summary = raw_output[keyword_pos + len(keyword):].strip()
        cleaned_lines = [line for line in summary.splitlines() if line.strip()]
        return "\n".join(cleaned_lines)
    return raw_output.strip()


@app.route('/api/upload', methods=['POST'])
def upload_apk():
    """Upload APK file and start analysis"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only APK files allowed'}), 400
    
    # Generate unique ID for this analysis
    analysis_id = str(uuid.uuid4())
    file_bytes = file.read()
    filename = secure_filename(file.filename)
    
    # Save file temporarily
    temp_path = os.path.join(UPLOAD_FOLDER, f"{analysis_id}_{filename}")
    with open(temp_path, 'wb') as f:
        f.write(file_bytes)
    
    # Initialize analysis result
    analysis_results[analysis_id] = {
        'status': 'processing',
        'filename': filename,
        'created_at': datetime.now().isoformat(),
        'ml_results': None,
        'mobsf_report': None,
        'llm_summaries': None,
        'error': None
    }
    
    # # Stage 1: Fast path - ML Prediction (synchronous)
    # try:
    #     permissions = extract_permissions_via_subprocess(temp_path)
    #     ml_results = run_ml_predictions(permissions, ml_models, feature_columns, model_accuracies)
    #     analysis_results[analysis_id]['ml_results'] = ml_results
    # except Exception as e:
    #     analysis_results[analysis_id]['ml_results'] = []
    #     analysis_results[analysis_id]['error'] = f"ML step failed: {e}"

    # Stage 2+3: Slow path - MobSF + LLM (run in background thread)
    def _deep_analysis_task():
        try:
            # MobSF Analysis (optional)
            try:
                hash_file = sha1(file_bytes).hexdigest()
                if hash_file in analyzed_apk.keys():
                    report = generate_json_report(analyzed_apk[hash_file])
                else:
                    upload_response = upload_file_to_mobsf(filename, file_bytes)
                    start_scan(upload_response)
                    analyzed_apk[hash_file] = upload_response["hash"]
                    report = generate_json_report(upload_response["hash"])
                permissions = list(report['permissions'].keys())
                ml_results = run_ml_predictions(permissions, ml_models, feature_columns, model_accuracies)
                analysis_results[analysis_id]['ml_results'] = ml_results
                with open(REPORT_PATH, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2)
                analysis_results[analysis_id]['mobsf_report'] = report
            except Exception as e:
                print(f"MobSF analysis failed: {e}")
                analysis_results[analysis_id]['mobsf_error'] = str(e)

            # LLM Analysis (optional)
            try:
                perm_script_path = os.path.join(BASE_DIR, "Permission Extracter", "permission_to_LLM.py")
                api_script_path = os.path.join(BASE_DIR, "sesitive APIs", "sensitiveAPI_to_LLM.py")

                perm_result = subprocess.run(
                    [PYTHON_VENV_PATH, perm_script_path],
                    capture_output=True,
                    text=True,
                    check=False,
                    encoding='utf-8'
                )
                api_result = subprocess.run(
                    [PYTHON_VENV_PATH, api_script_path],
                    capture_output=True,
                    text=True,
                    check=False,
                    encoding='utf-8'
                )

                analysis_results[analysis_id]['llm_summaries'] = {
                    "permissions": parse_summary(perm_result.stdout),
                    "sensitive_api": parse_summary(api_result.stdout)
                }
            except Exception as e:
                print(f"LLM analysis failed: {e}")

            analysis_results[analysis_id]['status'] = 'completed'
        except Exception as e:
            analysis_results[analysis_id]['status'] = 'error'
            analysis_results[analysis_id]['error'] = str(e)
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass

    threading.Thread(target=_deep_analysis_task, daemon=True).start()

    # Return immediately with ML results available, while deep analysis continues
    return jsonify({
        'analysis_id': analysis_id,
        'status': analysis_results[analysis_id]['status'],
        'ml_results': analysis_results[analysis_id]['ml_results'],
        'message': 'Analysis started. ML results ready; MobSF & LLM running in background.'
    }), 202


@app.route('/api/analysis/<analysis_id>', methods=['GET'])
def get_analysis_status(analysis_id):
    """Get analysis status and results"""
    if analysis_id not in analysis_results:
        return jsonify({'error': 'Analysis not found'}), 404
    
    result = analysis_results[analysis_id].copy()
    return jsonify(result), 200


@app.route('/api/report/latest', methods=['GET'])
def get_latest_report():
    """Get the latest analysis report (for frontend compatibility)"""
    if not analysis_results:
        return jsonify({'error': 'No reports available'}), 404
    
    # Get most recent analysis
    latest_id = max(analysis_results.keys(), key=lambda k: analysis_results[k]['created_at'])
    result = analysis_results[latest_id].copy()
    return jsonify(result), 200


@app.route('/api/report/<analysis_id>', methods=['GET'])
def get_report(analysis_id):
    """Get specific analysis report"""
    if analysis_id not in analysis_results:
        return jsonify({'error': 'Analysis not found'}), 404
    
    result = analysis_results[analysis_id].copy()
    return jsonify(result), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': len(ml_models),
        'feature_columns': len(feature_columns) if feature_columns else 0
    }), 200

@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")


if __name__ == '__main__':
    import socket
    
    # Get local IP address for display
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "localhost"
    
    local_ip = get_local_ip()
    port = 5000
    
    print("\n" + "="*50)
    print("🚀 APKTrust Flask API Server")
    print("="*50)
    print(f"📁 Base directory: {BASE_DIR}")
    print(f"📤 Upload folder: {UPLOAD_FOLDER}")
    print(f"📊 Output folder: {OUTPUT_FILES_DIR}")
    print(f"🤖 Models loaded: {len(ml_models)}/{len(MODEL_NAMES)}")
    print("="*50)
    print(f"\n🌐 Server accessible at:")
    print(f"   Local:   http://localhost:{port}")
    print(f"   Network: http://{local_ip}:{port}")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)

