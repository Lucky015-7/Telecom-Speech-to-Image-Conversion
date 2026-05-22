"""
Streamlit Frontend for Voice-to-Image Generation System
SLT Mobitel Research Project - Production Version
"""

import streamlit as st
import requests
from PIL import Image
import io
import time
from pathlib import Path
import json

# --- PAGE CONFIGURATION ---
# Sets up the custom browser tab icon, title, and forces a widescreen layout
st.set_page_config(
    page_title="Voice-to-Image | SLT Mobitel",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS STYLING (SLT BRANDING) ---
# Embeds custom corporate styles to mirror SLT Mobitel's design palette
st.markdown("""
<style>
    /* Main theme colors - SLT Mobitel branding */
    :root {
        --primary-color: #E31837;
        --secondary-color: #1E3A8A;
        --accent-color: #10B981;
        --background-color: #F8FAFC;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #E31837 0%, #1E3A8A 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Card styling */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #E31837;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1E3A8A;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748B;
        margin-top: 0.5rem;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #E31837 0%, #B91C2E 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(227, 24, 55, 0.4);
    }
    
    /* File uploader styling */
    .uploadedFile {
        border: 2px dashed #E31837;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Success message */
    .success-message {
        background: #D1FAE5;
        color: #065F46;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #10B981;
        margin: 1rem 0;
    }
    
    /* Image container */
    .image-container {
        border: 2px solid #E5E7EB;
        border-radius: 10px;
        padding: 1rem;
        background: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Feature badge */
    .feature-badge {
        display: inline-block;
        background: #E31837;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #E31837 0%, #1E3A8A 100%);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-weight: 600;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #64748B;
        font-size: 0.9rem;
        margin-top: 3rem;
        border-top: 1px solid #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)

# --- BACKEND LINKAGE CONSTANTS ---
API_BASE_URL = "http://127.0.0.1:8000"

# --- SESSION STATE INITIALIZATION ---
# Automatically instantiates a persistent collection tracking user transaction history blocks
if 'processing_history' not in st.session_state:
    st.session_state.processing_history = []

# --- HELPER UTILITY MODULES ---


def check_api_health():
    """Verifies connection integrity with background computing nodes."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def process_audio(audio_file, mode):
    """Pipes incoming audio multipart payloads to the correct API endpoint."""
    endpoint = f"{API_BASE_URL}/api/v1/process-audio"
    files = {"file": (audio_file.name, audio_file.getvalue(), audio_file.type)}

    try:
        response = requests.post(endpoint, files=files, timeout=300)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Connection Error: {str(e)}")
        return None


def get_image(filename_path):
    """Retrieves generated binary file-system images from backend storage paths."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/v1/fetch-image?path={filename_path}", timeout=30)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content))
    except:
        return None


# --- BRANDED APPLICATION MAIN HEADER ---
st.markdown("""
<div class="main-header">
    <h1>🎙️ Voice-to-Image Generation System</h1>
    <p>Intelligent Voice Understanding Platform for Telecom Customer Service</p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">
        <strong>SLT Mobitel Research Project</strong> | ConnectPlus ISP Domain
    </p>
</div>
""", unsafe_allow_html=True)

# --- API NETWORK HEALTH SANITY CHECK ---
api_status = check_api_health()
if not api_status:
    st.error("⚠️ Backend API is not running. Please start your FastAPI backend architecture service first.")
    st.code("python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload", language="bash")
    st.stop()

# --- SIDEBAR CONTROL PANEL CONTAINER ---
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/E31837/FFFFFF?text=SLT+Mobitel",
             use_container_width=True)

    st.markdown("### 🎯 Configuration Panel")
    st.info("⚡ System updated to prioritize high-fidelity generation via Method B pipeline structures.")

    st.markdown("---")
    st.markdown("### 📊 System Status Dashboard")
    st.info(f"✅ API Status: **Online**\n\n🖥️ Compute Unit: **Active**\n\n🤖 Pipeline State: **Models Loaded**")

    st.markdown("---")
    st.markdown("### 📚 Domain Coverage")
    st.markdown("""
    This platform translates spoken customer calls straight into actionable imagery representing technical site errors.
    
    **Supported Incident Areas:**
    - 🌐 Broadband Connections
    - 📺 Set-Top Box & TV Signal Drops
    - 🔧 Infrastructure Cable Failures
    """)

# --- MAIN WORKSPACE TAB CONTROLLERS ---
tab1, tab2, tab3 = st.tabs(
    ["🎙️ Process Recording", "📊 History Dashboard", "ℹ️ System Documentation"])

with tab1:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📤 Upload Incident Audio")
        audio_file = st.file_uploader(
            "Choose a customer voice recording clip",
            type=["mp3", "wav", "mpeg", "m4a", "flac"],
            help="Upload the audio sample to run transcription and scene generation modeling."
        )

        if audio_file:
            st.audio(
                audio_file, format=f"audio/{audio_file.type.split('/')[-1]}")

            st.markdown(f"""
            <div class="info-card">
                <strong>📁 File Signature:</strong> {audio_file.name}<br>
                <strong>衡量 File Size:</strong> {audio_file.size / 1024:.2f} KB<br>
                <strong>🎵 Content Type:</strong> {audio_file.type}
            </div>
            """, unsafe_allow_html=True)

            if st.button("🚀 Execute Visual Synthesis Pipeline", type="primary"):
                # Initialize visual loading status indicators
                progress_bar = st.progress(0)
                status_text = st.empty()

                status_text.text(
                    "📥 Staging raw audio sample to computing cluster...")
                progress_bar.progress(20)

                # Fire network execution command
                result = process_audio(audio_file, mode="B")

                if result and result.get('status') == 'success':
                    status_text.text(
                        "🗣️ Running Whisper ASR and SDXL model matrices...")
                    progress_bar.progress(60)
                    time.sleep(0.5)

                    status_text.text(
                        "🎨 Finalizing high-resolution rendering canvas...")
                    progress_bar.progress(100)

                    # Log successful generation outcomes to the runtime memory session state
                    st.session_state.current_result = result
                    st.session_state.processing_history.append({
                        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                        'filename': audio_file.name,
                        'result': result
                    })

                    st.success(
                        "✅ Scene map model generation completed successfully!")
                    st.rerun()
                else:
                    st.error(
                        "❌ High-fidelity pipeline processing sequence failed. Verify hardware device capacity.")
                    progress_bar.empty()
                    status_text.empty()

    with col2:
        st.markdown("### 🖼️ Synthesized Operational Output")

        if 'current_result' in st.session_state:
            result = st.session_state.current_result
            image = get_image(result['image_path'])

            if image:
                st.markdown('<div class="image-container">',
                            unsafe_allow_html=True)
                st.image(image, use_container_width=True,
                         caption="Generated Scene Model Frame")
                st.markdown('</div>', unsafe_allow_html=True)

                # Construct an in-memory binary tracking buffer download utility button
                img_buffer = io.BytesIO()
                image.save(img_buffer, format='PNG')
                st.download_button(
                    label="💾 Export Generated PNG Map",
                    data=img_buffer.getvalue(),
                    file_name=f"SLT_Export_{time.time_ns()}.png",
                    mime="image/png",
                    use_container_width=True
                )

            st.markdown("---")
            st.markdown("### 📈 Analytical Diagnostics")

            # Displays telemetry calculations layout
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{result['metrics']['energy']}</div>
                    <div class="metric-label">Signal RMS Loudness</div>
                </div>
                """, unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{result['metrics']['brightness']}</div>
                    <div class="metric-label">Spectral Brightness</div>
                </div>
                """, unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{result['metrics']['zcr']}</div>
                    <div class="metric-label">Zero-Crossing Rate</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("#### 📝 Parsed Customer Transcript Context")
            st.info(result['transcript'])
        else:
            st.info(
                "☝️ Please upload an incident clip and select execute to evaluate results in this panel view context.")

with tab2:
    st.markdown("### 📊 Enterprise Logging History")

    if st.session_state.processing_history:
        for i, entry in enumerate(reversed(st.session_state.processing_history), 1):
            with st.expander(f"🕐 Record #{i} | {entry['timestamp']} - File: {entry['filename']}"):
                h_col1, h_col2 = st.columns([1, 2])

                with h_col1:
                    hist_image = get_image(entry['result']['image_path'])
                    if hist_image:
                        st.image(hist_image, use_container_width=True)

                with h_col2:
                    st.markdown("**Verbatim Conversation Text Output:**")
                    st.info(entry['result']['transcript'])

                    st.markdown("**Telemetry Signature Indices:**")
                    st.json(entry['result']['metrics'])

        if st.button("🗑️ Purge Workspace Session History Logs", type="secondary", use_container_width=True):
            st.session_state.processing_history = []
            st.rerun()
    else:
        st.info("No logs cataloged in current running instance sequence space yet.")

with tab3:
    st.markdown("### 📖 Technical Specification Overview")
    doc_col1, doc_col2 = st.columns(2)

    with doc_col1:
        st.markdown("""
        #### 🎯 Functional Objectives
        This multi-layered engine converts customer voice inputs regarding field network errors directly into sharp visual context representations. This helps operations managers immediately classify equipment fault contexts visually.
        
        #### ⚙️ Upgraded Engine Components
        - **ASR Layer**: Whisper Large-v3 Turbo (captures high localized language metrics).
        - **Generative Synthesis Layer**: Stable Diffusion XL Base (outputs native 1024x1024 photographic detail layout maps).
        """)

    with doc_col2:
        st.markdown("""
        #### 📊 Signal Characteristic Arrays
        - **RMS Loudness**: Quantifies signal sound wave amplitude constraints.
        - **Spectral Centroid**: Tracks signal frequency centroid to locate noise distortion properties.
        - **Zero-Crossing Rate**: Evaluates fricative vocal characteristics to parse speech context cleanly.
        """)

# --- CORPORATE REPO FOOTER CARD ---
st.markdown("""
<div class="footer">
    <strong>Voice-to-Image Generation System v3.0</strong><br>
    SLT Mobitel Research Project Portfolio Pipeline | 2026<br>
    Intelligent Voice Understanding Platform for Telecom Customer Service<br>
    <em>ConnectPlus ISP Domain Architecture</em>
</div>
""", unsafe_allow_html=True)
