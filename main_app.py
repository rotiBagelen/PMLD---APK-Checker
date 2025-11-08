# D:\apktrust\main_app.py (Halaman Depan / Landing Page)

import streamlit as st
import time

# Konfigurasi halaman
st.set_page_config(
    page_title="APKTrust Home",
    page_icon="🛡️",
    layout="centered" # Menggunakan layout centered untuk halaman depan
)

# Sembunyikan UI bawaan Streamlit untuk tampilan yang lebih bersih
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Inisialisasi session state untuk menyimpan data antar halaman
if 'uploaded_file_data' not in st.session_state:
    st.session_state['uploaded_file_data'] = None

# --- UI Halaman Depan ---
st.title("🛡️ APKTrust")
st.subheader("A modern mobile application for digital trust & security verification.")
st.write("")
st.write("")

uploaded_apk = st.file_uploader(
    "UPLOAD YOUR APP HERE!",
    type=["apk"],
    label_visibility="collapsed"
)

if uploaded_apk is not None:
    # Simpan file yang diunggah (dalam bentuk bytes) dan namanya ke session state
    st.session_state['uploaded_file_data'] = {
        "name": uploaded_apk.name,
        "bytes": uploaded_apk.getvalue()
    }
    
    with st.spinner('File diterima, mengalihkan ke halaman analisis...'):
        time.sleep(1)
        # Pindah ke halaman laporan untuk memulai analisis
        st.switch_page("pages/Report.py")