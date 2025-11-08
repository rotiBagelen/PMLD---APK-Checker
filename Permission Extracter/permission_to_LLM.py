# permission_to_LLM.py (VERSI LENGKAP & DIPERBAIKI)
import json
import os
import time
from dotenv import load_dotenv
from groq import Groq

# === Load environment variables ===
load_dotenv()

# === CONFIGURATION ===
MOBSF_REPORT_PATH = "./output_files/mobsf_report.json"
CHUNK_SIZE = 100
MODEL = "llama-3.3-70b-versatile"

# === Init Groq client ===
# Pastikan GROQ_API_KEY ada di file .env Anda
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# === STEP 1: Extract Permissions from MobSF JSON ===
def extract_permissions(json_path):
    # Menambahkan pengecekan file di dalam fungsi agar lebih aman
    if not os.path.exists(json_path):
        print(f"[ERROR] File input tidak ditemukan: {json_path}")
        return []
        
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            report = json.load(file)

        permissions_data = report.get("permissions", {})
        if not permissions_data:
            print("[WARN] Tidak ada izin yang ditemukan di dalam laporan.")
            return []

        permissions = [f"- {perm_name}" for perm_name in permissions_data.keys()]
        print(f"[OK] Berhasil mengekstrak {len(permissions)} izin.")
        return permissions

    except json.JSONDecodeError:
        print(f"[ERROR] Format JSON tidak valid di file: {json_path}")
        return []
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan saat membaca file: {e}")
        return []

# === STEP 2: Chunk the Permission List ===
def chunk_permissions(permissions, chunk_size=CHUNK_SIZE):
    return ["\n".join(permissions[i:i + chunk_size]) for i in range(0, len(permissions), chunk_size)]

# === STEP 3: Call Groq LLM with Retry ===
def call_groq_llm(prompt, retries=3):
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[WARN] Percobaan {attempt + 1} gagal: {e}")
            time.sleep(2)
    return None

# === STEP 4: Analyze One Chunk ===
def analyze_permission_chunk(chunk_text):
    prompt = f"""You are a mobile security analyst. Analyze the following Android app permissions from a security and privacy standpoint.

For each permission:
- Explain its purpose in simple terms.
- Analyze how it can be abused or misused.
- Determine if it's sensitive or overprivileged.

At the end, provide:
- A summary of risky combinations (e.g., Internet + SMS)
- An overall risk rating
- Recommendations to developers or users

Write your analysis in Bahasa Indonesia, no JSON, only in bulleted point, no need any additional intro text.

Permissions:
{chunk_text}
"""
    return call_groq_llm(prompt)

# === STEP 5: Generate Executive Summary from All Results ===
def generate_summary(results):
    if not results:
        return "Tidak ada hasil analisis untuk diringkas."
    
    combined_text = "\n\n---\n\n".join(results)
    summary_prompt = f"""You are an Android security consultant. Based on this analysis, give a plain-text executive summary.

Analysis:
{combined_text}

Write 3 bullet points summarizing the overall security risks, user impact, and developer recommendations.
Avoid using technical terms or JSON.
"""
    return call_groq_llm(summary_prompt)

# === MAIN ===
def main():
    # PERBAIKAN: Menghapus ')' tambahan dan emoji
    print("\nStarting permission analysis...")

    permissions = extract_permissions(MOBSF_REPORT_PATH)
    if not permissions:
        return

    chunks = chunk_permissions(permissions)
    results = []

    # PERBAIKAN: Menghapus emoji
    print(f"Analyzing {len(chunks)} permission chunk(s)...\n")
    for i, chunk in enumerate(chunks, 1):
        # PERBAIKAN: Menghapus emoji
        print(f"Analyzing chunk {i}/{len(chunks)}...")
        result = analyze_permission_chunk(chunk)
        if result:
            results.append(result)
        time.sleep(1) # Jeda antar request API

    # PERBAIKAN: Menghapus emoji
    print("\nGenerating final executive summary...\n")
    summary = generate_summary(results)

    # PERBAIKAN: Menghapus emoji
    print("\nExecutive Summary:")
    print(summary or "Tidak ada ringkasan yang tersedia.")

if __name__ == "__main__":
    main()