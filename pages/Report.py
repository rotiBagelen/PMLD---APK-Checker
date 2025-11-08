# D:\apktrust\pages\Report.py (Halaman Laporan Final yang Digabungkan)

import streamlit as st
import pandas as pd
import json
import os
import sys
import subprocess
import time
import requests
import joblib
import tempfile
from dotenv import load_dotenv

# --- KONFIGURASI DAN FUNGSI-FUNGSI ---

st.set_page_config(page_title="Analysis Report", page_icon="📊", layout="wide")
st.title("Detail Information — Analysis Report")

# Menentukan path absolut untuk file-file di direktori utama
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')

# Muat .env dari direktori utama
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))
API_KEY = os.getenv("API_KEY")
MOBSF_URL = os.getenv("MOBSF_URL", "http://localhost:8000")
PYTHON_VENV_PATH = sys.executable
MODEL_NAMES = ["RandomForest", "SVM", "GradientBoosting", "XGBoost"]
OUTPUT_FILES_DIR = os.path.join(BASE_DIR, "output_files")
REPORT_PATH = os.path.join(OUTPUT_FILES_DIR, "mobsf_report.json")

# Validate MobSF configuration
def validate_mobsf_config():
    """Check if MobSF API key and URL are configured"""
    issues = []
    if not API_KEY:
        issues.append("API_KEY is not set in .env file")
    if not MOBSF_URL or MOBSF_URL == "http://localhost:8000":
        issues.append(f"MOBSF_URL is set to default ({MOBSF_URL}). Ensure MobSF is running.")
    return issues

# --- (Fungsi-fungsi helper) ---
def upload_file_to_mobsf(file_name, file_bytes):
    """Upload APK file to MobSF and return upload response"""
    from requests_toolbelt.multipart.encoder import MultipartEncoder
    
    if not API_KEY:
        raise ValueError("API_KEY is not configured. Please set API_KEY in your .env file.")
    
    try:
        mp_encoder = MultipartEncoder(fields={'file': (file_name, file_bytes, 'application/octet-stream')})
        headers = {'Authorization': API_KEY, 'Content-Type': mp_encoder.content_type}
        response = requests.post(f"{MOBSF_URL}/api/v1/upload", data=mp_encoder, headers=headers, timeout=300)
        
        if response.status_code == 401:
            raise ValueError(
                f"❌ 401 Unauthorized - Invalid API key or MobSF authentication failed.\n\n"
                f"How to fix:\n"
                f"1. Make sure MobSF is running at {MOBSF_URL}\n"
                f"2. Get your API key from MobSF:\n"
                f"   - Open MobSF in browser: {MOBSF_URL}\n"
                f"   - Go to Settings → API Keys\n"
                f"   - Copy your API key\n"
                f"3. Add to .env file in project root:\n"
                f"   API_KEY=your_api_key_here\n"
                f"   MOBSF_URL=http://localhost:8000\n"
            )
        elif response.status_code == 404:
            raise ValueError(
                f"❌ 404 Not Found - MobSF endpoint not found.\n\n"
                f"Check if MobSF is running at {MOBSF_URL}\n"
                f"Make sure the URL is correct in your .env file."
            )
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            f"❌ Cannot connect to MobSF at {MOBSF_URL}\n\n"
            f"Make sure MobSF is running:\n"
            f"- If using Docker: docker run -p 8000:8000 opensecurity/mobsf\n"
            f"- Or start your local MobSF instance\n"
            f"Then verify it's accessible at {MOBSF_URL}"
        )

def start_scan(upload_data):
    """Start MobSF scan on uploaded file"""
    if not API_KEY:
        raise ValueError("API_KEY is not configured.")
    
    response = requests.post(f"{MOBSF_URL}/api/v1/scan", data=upload_data, headers={'Authorization': API_KEY}, timeout=300)
    if response.status_code == 401:
        raise ValueError("401 Unauthorized - Invalid API key for scan request.")
    response.raise_for_status()

def generate_json_report(hash_value):
    """Generate and retrieve JSON report from MobSF"""
    if not API_KEY:
        raise ValueError("API_KEY is not configured.")
    
    time.sleep(90)  # Wait for scan to complete
    response = requests.post(f"{MOBSF_URL}/api/v1/report_json", data={'hash': hash_value}, headers={'Authorization': API_KEY}, timeout=300)
    if response.status_code == 401:
        raise ValueError("401 Unauthorized - Invalid API key for report request.")
    response.raise_for_status()
    return response.json()

@st.cache_resource
def load_ml_assets():
    try:
        models = {name: joblib.load(os.path.join(BASE_DIR, f"{name.lower()}_model.joblib")) for name in MODEL_NAMES}
        feature_columns = joblib.load(os.path.join(BASE_DIR, "feature_columns.joblib"))
        with open(os.path.join(BASE_DIR, "model_accuracies.json"), 'r') as f: accuracies = json.load(f)
        return models, feature_columns, accuracies
    except FileNotFoundError as e:
        st.error(f"Model file not found: {e}")
        return None, None, None
    except Exception as e:
        error_msg = str(e)
        if "numpy._core" in error_msg:
            st.error(f"⚠️ NumPy version mismatch detected! Models may have been saved with a different NumPy version.\n\n"
                    f"Error: {error_msg}\n\n"
                    f"Please run: pip install --upgrade --force-reinstall 'numpy<2.0.0' 'scikit-learn>=1.3.0,<1.5.0' 'joblib>=1.3.0'\n\n"
                    f"If this persists, you may need to retrain the models with the current NumPy version.")
        elif "_loss" in error_msg or "sklearn._loss" in error_msg:
            st.error(f"⚠️ scikit-learn version mismatch detected! The '_loss' module error indicates incompatible scikit-learn versions.\n\n"
                    f"Error: {error_msg}\n\n"
                    f"Solution 1 (Recommended): Reinstall compatible versions:\n"
                    f"```bash\npip uninstall -y scikit-learn numpy joblib\npip install 'numpy<2.0.0' 'scikit-learn>=1.3.0,<1.5.0' 'joblib>=1.3.0'\n```\n\n"
                    f"Solution 2: Retrain models with current environment:\n"
                    f"```bash\npython train_and_save_models.py\n```")
        elif "ModuleNotFoundError" in error_msg:
            st.error(f"⚠️ Module import error detected!\n\n"
                    f"Error: {error_msg}\n\n"
                    f"Please ensure all dependencies are installed:\n"
                    f"```bash\npip install -r requirements.txt\n```")
        else:
            st.error(f"Error loading ML models: {error_msg}\n\n"
                    f"This might be a version compatibility issue. Try:\n"
                    f"1. Reinstalling: pip install --force-reinstall 'scikit-learn>=1.3.0,<1.5.0' 'joblib>=1.3.0'\n"
                    f"2. Retraining models: python train_and_save_models.py")
        return None, None, None

def extract_permissions_via_subprocess(apk_path):
    try:
        script_path = os.path.join(BASE_DIR, "extract_permissions.py")
        result = subprocess.run([PYTHON_VENV_PATH, script_path, apk_path], capture_output=True, text=True, check=False, encoding='utf-8')
        
        if result.returncode != 0:
            error_msg = result.stderr.strip() or result.stdout.strip()
            st.error(f"Permission extractor failed (exit code {result.returncode}): {error_msg}")
            return set()
        
        # Extract JSON from stdout - handle cases where there might be extra output
        stdout = result.stdout.strip()
        if not stdout:
            st.warning("⚠️ Permission extractor returned empty output")
            return set()
        
        # Find the first JSON object in the output (in case there are warnings before it)
        json_start = stdout.find('{')
        if json_start == -1:
            st.error(f"Failed to find JSON in output. Raw output: {stdout[:200]}")
            return set()
        
        # Try to parse from the JSON start position
        json_str = stdout[json_start:]
        # Find the end of the JSON object (last closing brace before any trailing text)
        try:
            # Try to parse the entire remaining string first
            data = json.loads(json_str)
        except json.JSONDecodeError:
            # If that fails, try to find the complete JSON object
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
                raise json.JSONDecodeError("Could not find complete JSON object", json_str, 0)
        
        if "error" in data:
            st.error(f"Permission extraction error: {data['error']}")
            return set()
        
        permissions_list = data.get("permissions", [])
        if len(permissions_list) == 0:
            st.warning("⚠️ No permissions found in APK. This may be normal for some apps, but could indicate an extraction issue.")
        else:
            st.success(f"✓ Extracted {len(permissions_list)} permissions from APK")
        return set(permissions_list)
        
    except json.JSONDecodeError as e:
        st.error(f"Failed to parse permission extraction output: {e}\n"
                f"Raw stdout: {result.stdout[:500] if 'result' in locals() else 'N/A'}\n"
                f"Raw stderr: {result.stderr[:200] if 'result' in locals() and result.stderr else 'N/A'}")
        return set()
    except Exception as e:
        st.error(f"Unexpected error during permission extraction: {str(e)}")
        return set()

def normalize_permission_for_matching(permission):
    """
    Normalize permission names to match training data format.
    Training data typically uses short uppercase names (e.g., 'INTERNET')
    while androguard returns full names (e.g., 'android.permission.INTERNET')
    """
    if not permission:
        return ""
    # Remove common Android permission prefixes
    normalized = permission.strip()
    if normalized.startswith("android.permission."):
        normalized = normalized.replace("android.permission.", "")
    elif normalized.startswith("com.android."):
        normalized = normalized.replace("com.android.", "")
    # Convert to uppercase for consistency
    normalized = normalized.upper()
    return normalized

def run_ml_predictions(permissions_set, models, feature_columns, accuracies):
    # Normalize permissions for matching (fixes format mismatch)
    normalized_perms = {normalize_permission_for_matching(perm): perm for perm in permissions_set}
    normalized_perms_set = set(normalized_perms.keys())
    
    # Try both original and normalized matching to find best strategy
    matched_features_original = sum(1 for col in feature_columns if col in permissions_set)
    matched_features_normalized = sum(1 for col in feature_columns if normalize_permission_for_matching(col) in normalized_perms_set or col in normalized_perms_set)
    
    # Use the best matching strategy
    use_normalized = matched_features_normalized > matched_features_original
    
    # Detailed diagnostics
    with st.expander("🔍 Diagnostic Information (Click to expand)", expanded=False):
        st.write(f"**Extracted Permissions:** {len(permissions_set)}")
        if len(permissions_set) > 0:
            st.write("Sample extracted permissions (first 10):")
            sample_perms = sorted(list(permissions_set))[:10]
            st.code("\n".join(sample_perms))
            st.write("Sample normalized permissions:")
            sample_normalized = sorted(list(normalized_perms_set))[:10]
            st.code("\n".join(sample_normalized))
        
        st.write(f"**Model Feature Columns:** {len(feature_columns)}")
        st.write("Sample feature columns (first 10):")
        st.code("\n".join(feature_columns[:10]))
        
        # Check matching with both methods
        matched_features = matched_features_normalized if use_normalized else matched_features_original
        
        st.write(f"**Matched Features (original):** {matched_features_original}/{len(feature_columns)}")
        st.write(f"**Matched Features (normalized):** {matched_features_normalized}/{len(feature_columns)}")
        st.write(f"**Using:** {'Normalized matching' if use_normalized else 'Original matching'}")
        
        if matched_features > 0:
            matched_perms = [col for col in feature_columns 
                            if (use_normalized and (normalize_permission_for_matching(col) in normalized_perms_set or col in normalized_perms_set))
                            or (not use_normalized and col in permissions_set)]
            st.write("Matched permissions:")
            st.code("\n".join(matched_perms[:10]))
        
        # Show mismatches
        if len(permissions_set) > 0 and matched_features == 0:
            st.error("⚠️ **CRITICAL MISMATCH DETECTED!**")
            st.write("Extracted permissions don't match any feature columns. This will cause all-zero feature vectors!")
            st.write("**Sample extracted (original):**")
            sample_extracted = sorted(list(permissions_set))[:5]
            st.code("\n".join(sample_extracted))
            st.write("**Sample extracted (normalized):**")
            sample_norm = sorted(list(normalized_perms_set))[:5]
            st.code("\n".join(sample_norm))
            st.write("**Sample expected (from features):**")
            st.code("\n".join(feature_columns[:5]))
    
    # Diagnostic: Check if permissions were extracted
    if len(permissions_set) == 0:
        st.error("⚠️ **No permissions extracted from APK!** Feature vector will be all zeros, which will cause incorrect predictions.")
        st.info("This means the permission extraction is failing. Check the extract_permissions.py script.")
    
    # Create feature vector using the best matching strategy
    row = {}
    for col in feature_columns:
        col_normalized = normalize_permission_for_matching(col)
        if use_normalized:
            # Try normalized matching
            if col in normalized_perms_set or col_normalized in normalized_perms_set or col.upper() in normalized_perms_set:
                row[col] = 1
            else:
                row[col] = 0
        else:
            # Try original matching
            if col in permissions_set:
                row[col] = 1
            else:
                row[col] = 0
    prediction_df = pd.DataFrame([row], columns=feature_columns)
    
    # Diagnostic: Show feature vector stats
    feature_sum = sum(row.values())
    if feature_sum == 0:
        st.error("🚨 **CRITICAL: All features are zero!** The model will always predict the same result regardless of APK.")
        st.error("**This confirms the problem - no features are being activated.**")
    else:
        st.success(f"✓ Feature vector has {feature_sum} active features out of {len(feature_columns)} total")
    
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
            pred_text = "Waspada"
            pred_category = "warning"
        else:
            pred_text = "Berbahaya"
            pred_category = "dangerous"
        
        results.append({
            "Model": name,
            "Hasil Prediksi": pred_text,
            "Kepercayaan (Berbahaya)": confidence,
            "Akurasi (saat Training)": accuracies.get(name, 0),
            "Kategori": pred_category  # Optional: store category for styling
        })
    return pd.DataFrame(results)

def parse_summary(raw_output: str) -> str:
    keyword = "executive summary:"
    lower_output = raw_output.lower()
    keyword_pos = lower_output.rfind(keyword)
    if keyword_pos != -1:
        summary = raw_output[keyword_pos + len(keyword):].strip()
        cleaned_lines = [line for line in summary.splitlines() if line.strip()]
        return "\n".join(cleaned_lines)
    return raw_output.strip()

# --- FUNGSI UTAMA UNTUK MENJALANKAN SEMUA ANALISIS ---
def run_all_analyses(file_data):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".apk") as tmp:
        tmp.write(file_data['bytes'])
        temp_apk_path = tmp.name

    with st.status("Memulai analisis lengkap...", expanded=True) as status:
        # TAHAP 1
        status.update(label="1/3: Menjalankan prediksi cepat dengan model Machine Learning...")
        ml_models, feature_columns, model_accuracies = load_ml_assets()
        if ml_models:
            permissions = extract_permissions_via_subprocess(temp_apk_path)
            st.session_state['ml_results'] = run_ml_predictions(permissions, ml_models, feature_columns, model_accuracies)

        # TAHAP 2
        status.update(label="2/3: Menjalankan analisis mendalam dengan MobSF...")
        try:
            # Validate configuration before attempting MobSF operations
            config_issues = validate_mobsf_config()
            if config_issues:
                for issue in config_issues:
                    st.warning(f"⚠️ {issue}")
            
            os.makedirs(OUTPUT_FILES_DIR, exist_ok=True)
            upload_response = upload_file_to_mobsf(file_data['name'], file_data['bytes'])
            start_scan(upload_response)
            report = generate_json_report(upload_response["hash"])
            with open(REPORT_PATH, 'w', encoding='utf-8') as f: json.dump(report, f, indent=2)
            st.session_state['mobsf_report'] = report
            st.success("✓ MobSF analysis completed successfully")
        except ValueError as e:
            # Configuration or authentication errors
            st.error(str(e))
            st.info("💡 Tip: MobSF analysis is optional. ML predictions above are still valid.")
        except ConnectionError as e:
            # Connection errors
            st.error(str(e))
            st.info("💡 Tip: Make sure MobSF is running, or continue without MobSF analysis.")
        except Exception as e:
            error_msg = str(e)
            st.error(f"Analisis MobSF gagal: {error_msg}")
            if "401" in error_msg or "Unauthorized" in error_msg:
                st.info("💡 Check your API_KEY in the .env file. Get it from MobSF Settings → API Keys")
            else:
                st.info("💡 MobSF analysis is optional. ML predictions are still available.")

        # TAHAP 3
        status.update(label="3/3: Menjalankan analisis ringkasan dengan AI...")
        try:
            perm_script_path = os.path.join(BASE_DIR, "Permission Extracter", "permission_to_LLM.py")
            api_script_path = os.path.join(BASE_DIR, "sesitive APIs", "sensitiveAPI_to_LLM.py")
            perm_result = subprocess.run([PYTHON_VENV_PATH, perm_script_path], capture_output=True, text=True, check=True, encoding='utf-8')
            api_result = subprocess.run([PYTHON_VENV_PATH, api_script_path], capture_output=True, text=True, check=True, encoding='utf-8')
            st.session_state['llm_summaries'] = {
                "permissions": parse_summary(perm_result.stdout),
                "sensitive_api": parse_summary(api_result.stdout)
            }
        except Exception as e: st.error(f"Analisis AI gagal: {e}")

        status.update(label="Semua analisis selesai!", state="complete", expanded=False)

    os.remove(temp_apk_path)
    st.session_state['analysis_done'] = True

# --- UI HALAMAN LAPORAN ---
if not st.session_state.get('uploaded_file_data'):
    st.warning("Silakan kembali ke Halaman Utama untuk mengunggah file APK terlebih dahulu.")
    if st.button("Back to Home"): st.switch_page("main_app.py")
else:
    if not st.session_state.get('analysis_done'):
        run_all_analyses(st.session_state['uploaded_file_data'])

    ml_results_df = st.session_state.get('ml_results')
    report = st.session_state.get('mobsf_report')
    llm_summaries = st.session_state.get('llm_summaries')

    st.header("Hasil Prediksi 4 Model Machine Learning")
    if ml_results_df is not None and not ml_results_df.empty:
        st.dataframe(ml_results_df, hide_index=True, use_container_width=True,
            column_config={
                "Kepercayaan (Berbahaya)": st.column_config.ProgressColumn("Kepercayaan (Berbahaya)", format="%.2f", min_value=0, max_value=1),
                "Akurasi (saat Training)": st.column_config.ProgressColumn("Akurasi (saat Training)", format="%.2f", min_value=0, max_value=1),
            })
    else:
        st.info("Tidak ada hasil prediksi ML untuk ditampilkan.")

    st.divider()

    st.header("Ringkasan Berbasis AI")
    if llm_summaries:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Analisis Izin")
            st.markdown(llm_summaries.get("permissions", "Tidak ada ringkasan."))
        with col2:
            st.subheader("Analisis API Sensitif")
            st.markdown(llm_summaries.get("sensitive_api", "Tidak ada ringkasan."))
    else:
        st.info("Tidak ada ringkasan AI untuk ditampilkan.")

    st.divider()
    
    st.header("Detail Teknis dari MobSF")
    
    # Try to load report from session state or file
    if not report:
        # Try loading from file if not in session state
        if os.path.exists(REPORT_PATH):
            try:
                with open(REPORT_PATH, 'r', encoding='utf-8') as f:
                    report = json.load(f)
                    st.session_state['mobsf_report'] = report
                    st.info("ℹ️ Loaded MobSF report from file")
            except Exception as e:
                st.warning(f"⚠️ Could not load MobSF report from file: {e}")
    
    if report:
        st.subheader("Izin Aplikasi (Permissions)")
        permissions_data = report.get("permissions", {})
        
        # Debug info in expander
        with st.expander("🔍 MobSF Report Debug Info", expanded=False):
            st.write(f"**Report loaded:** ✅")
            st.write(f"**Report type:** {type(report).__name__}")
            st.write(f"**Has 'permissions' key:** {'permissions' in report}")
            st.write(f"**Permissions data type:** {type(permissions_data).__name__}")
            st.write(f"**Number of permissions:** {len(permissions_data) if isinstance(permissions_data, dict) else 'N/A'}")
            if isinstance(permissions_data, dict) and len(permissions_data) > 0:
                st.write("**Sample permission keys:**")
                st.code("\n".join(list(permissions_data.keys())[:5]))
        
        if permissions_data and isinstance(permissions_data, dict) and len(permissions_data) > 0:
            perm_list = []
            for name, details in permissions_data.items():
                # Handle case where details might be dict or other format
                if isinstance(details, dict):
                    status = details.get("status", "normal")
                    status_emoji = "🔴" if status == "dangerous" else ("🟠" if status == "warning" else "🟢")
                    perm_list.append({
                        "STATUS": f"{status_emoji} {status.capitalize()}",
                        "PERMISSION": name,
                        "INFO": details.get("info", ""),
                        "DESCRIPTION": details.get("description", "")
                    })
                else:
                    # If details is not a dict, just show the permission name
                    perm_list.append({
                        "STATUS": "🟢 Normal",
                        "PERMISSION": name,
                        "INFO": str(details) if details else "",
                        "DESCRIPTION": ""
                    })
            
            if perm_list:
                st.dataframe(pd.DataFrame(perm_list), hide_index=True, use_container_width=True)
                st.success(f"✓ Displayed {len(perm_list)} permissions from MobSF analysis")
            else:
                st.warning("⚠️ No permissions found in MobSF report (permissions_data is empty dict)")
        elif permissions_data is None or (isinstance(permissions_data, dict) and len(permissions_data) == 0):
            st.warning("⚠️ No permissions found in MobSF report. This could mean:")
            st.write("- The APK declares no permissions (unusual but possible)")
            st.write("- MobSF analysis did not extract permissions correctly")
            st.write("- The report structure is different than expected")
            
            # Show what we do have
            if isinstance(report, dict):
                st.write(f"\n**Available report keys:** {', '.join(list(report.keys())[:10])}")
        else:
            st.error(f"⚠️ Unexpected permissions data format: {type(permissions_data)}")
            st.code(str(permissions_data)[:500])
    else:
        st.info("ℹ️ MobSF report not available. This could mean:")
        st.write("- MobSF analysis was not performed (optional)")
        st.write("- MobSF analysis failed silently")
        st.write("- Report file was not generated")
        
        # Check if file exists
        if os.path.exists(REPORT_PATH):
            st.info(f"📄 Report file exists at: {REPORT_PATH}")
            st.info("Try refreshing the page or re-running the analysis.")
    
    if st.button("Analyze Another APK", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("main_app.py")