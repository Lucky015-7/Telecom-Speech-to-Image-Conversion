"""
Streamlit Frontend for Voice-to-Image Generation System
SLT Mobitel Research Project - Resolved Production Version
"""

import streamlit as st
import requests
from PIL import Image
import io
import time
from pathlib import Path
import json

# --- PAGE CONFIGURATION ---
# Configures the tab styling, browser title, and wide layout interface
st.set_page_config(
    page_title="Voice-to-Image | SLT Mobitel",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS STYLING (SLT BRANDING MATRICES) ---
# Embeds core styling properties matching SLT Mobitel's corporate identity palette
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

# --- INSTANCE SERVER ADRESSING ---
# Shared configuration reference point for mapping microservices communications
API_URL = "http://127.0.0.1:8000"

# --- RUNTIME MEMORY STATE MANAGMENT ---
# Verifies and instantiates local runtime list caches to retain processing tracking values
if 'processing_history' not in st.session_state:
    st.session_state.processing_history = []

# --- INTEGRATED SERVICE CORE API CONNECTIONS ---
def check_api_health():
    """Validates the background FastAPI core application engine status mapping."""
    try:
        # Pings the primary core route domain block to test connection loops
        response = requests.get(API_URL, timeout=5)
        return response.status_code == 200
    except:
        return False

def process_audio(audio_file):
    """Pipes multipart form boundary data chunks over standard network endpoints."""
    endpoint = f"{API_URL}/api/v1/process-audio"
    multipart_payload = {"file": (audio_file.name, audio_file.getvalue(), audio_file.type)}
    
    try:
        response = requests.post(endpoint, files=multipart_payload, timeout=300)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Core Microservice Connection Interrupted: {str(e)}")
        return None

def get_image(image_storage_path):
    """Fetches high-resolution visual targets from backend disk file layouts over parameters."""
    try:
        image_request_url = f"{API_URL}/api/v1/fetch-image?path={image_storage_path}"
        response = requests.get(image_request_url, timeout=30)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content))
    except:
        return None

# --- CORPORATE APPLICATION BANNER TOPMOST ---
st.markdown("""
<div class="main-header">
    <h1>🎙️ Voice-to-Image Generation System</h1>
    <p>Intelligent Voice Understanding Platform for Telecom Customer Service</p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">
        <strong>SLT Mobitel Research Project</strong> | ConnectPlus ISP Domain
    </p>
</div>
""", unsafe_allow_html=True)

# --- AUTOMATED API SYSTEM INTEGRITY GUARD ---
if not check_api_health():
    st.error("⚠️ Backend API Service Unavailable. Please boot your FastAPI infrastructure engine layers first.")
    st.code("python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload", language="bash")
    st.stop()

# --- SIDEBAR COMPONENT BLOCK CONTEXTS ---
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/E31837/FFFFFF?text=SLT+Mobitel", use_container_width=True)
    
    st.markdown("### 🎯 Core Optimization")
    st.success("⚙️ System adjusted to process production pipeline architectures via Speech-to-Text-to-Image mappings.")
    
    st.markdown("---")
    st.markdown("### 📊 Live Diagnostic Monitor")
    st.info(f"✅ Service Cluster: **Online**\n\n🖥️ Device Mode: **Hardware Ready**\n\n🤖 Deep Learning: **Models Loaded**")
    
    st.markdown("---")
    st.markdown("### 📚 About")
    st.markdown("""
    This analytics node interprets audio reporting clips from customer telephone service arrays to construct precise scene imagery representations of hardware or signal faults.
    """)

# --- INTERACTIVE CONTENT COMPONENT TABS ---
tab1, tab2, tab3 = st.tabs(["🎙️ Process Recording", "📊 History Logs Dashboard", "ℹ️ Engineering Documentation"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Upload Incident Audio")
        audio_file = st.file_uploader(
            "Select customer complaint sound segment file",
            type=["mp3", "wav", "mpeg", "m4a", "flac"],
            help="Ingests local container variants straight to underlying AI model stack pipelines."
        )
        
        if audio_file:
            st.audio(audio_file, format=f"audio/{audio_file.type.split('/')[-1]}")
            
            st.markdown(f"""
            <div class="info-card">
                <strong>📁 File Handle:</strong> {audio_file.name}<br>
                <strong>衡量 Binary Footprint:</strong> {audio_file.size / 1024:.2f} KB<br>
                <strong>🎵 Format Context:</strong> {audio_file.type}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Execute Visual Synthesis Pipeline", type="primary"):
                # Initialize application loading telemetry status structures
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("📥 Uploading client track across cluster array channels...")
                progress_bar.progress(25)
                
                # Execute pipeline request mapping tasks
                result = process_audio(audio_file)
                
                if result and result.get('status') == 'success':
                    status_text.text("🗣️ Instantiating high-accuracy Whisper ASR decoding & SDXL processing grids...")
                    progress_bar.progress(75)
                    time.sleep(0.3)
                    
                    status_text.text("✅ Rendering canvas structures completed successfully.")
                    progress_bar.progress(100)
                    
                    # Cache transaction payloads into global thread memory frameworks
                    st.session_state.current_result = result
                    st.session_state.processing_history.append({
                        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                        'filename': audio_file.name,
                        'result': result
                    })
                    
                    st.success("Analysis cycle dispatched safely.")
                    st.rerun()
                else:
                    st.error("❌ High-accuracy sequence failure encountered inside computing layers.")
                    progress_bar.empty()
                    status_text.empty()
                    
    with col2:
        st.markdown("### 🖼️ Synthesized Incident Mapping Canvas")
        
        if 'current_result' in st.session_state:
            result = st.session_state.current_result
            image = get_image(result['image_path'])
            
            if image:
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(image, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Setup binary safe image extraction transfer link buttons
                img_buffer = io.BytesIO()
                image.save(img_buffer, format='PNG')
                st.download_button(
                    label="💾 Export Generated Image File (PNG)",
                    data=img_buffer.getvalue(),
                    file_name=f"SLT_Export_{time.time_ns()}.png",
                    mime="image/png"
                )
            
            st.markdown("---")
            st.markdown("### 📈 Acoustic Waveform Signals Telemetry")
            
            # Formulates columns layout metric visualization interfaces
            metric_cols = st.columns(3)
            with metric_cols[0]:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{result['metrics']['energy']:.4f}</div>
                    <div class="metric-label">Signal RMS Loudness</div>
                </div>
                """, unsafe_allow_html=True)
            with metric_cols[1]:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{result['metrics']['brightness']:.2f}</div>
                    <div class="metric-label">Spectral Brightness</div>
                </div>
                """, unsafe_allow_html=True)
            with metric_cols[2]:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{result['metrics']['zcr']:.4f}</div>
                    <div class="metric-label">Zero-Crossing Rate</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("#### 📝 Verified Transcript Record Context Output")
            st.info(result['transcript'])
        else:
            st.info("☝️ Ingest an active user waveform track and trigger compilation models to visualize generation targets.")

with tab2:
    st.markdown("### 📊 Log Recording Audit Trails")
    
    if st.session_state.processing_history:
        for idx, entry in enumerate(reversed(st.session_state.processing_history), 1):
            with st.expander(f"🕐 Session Reference #{idx} | Timestamp: {entry['timestamp']} — File: {entry['filename']}"):
                hist_col1, hist_col2 = st.columns([1, 2])
                
                with hist_col1:
                    history_img = get_image(entry['result']['image_path'])
                    if history_img:
                        st.image(history_img, use_container_width=True)
                        
                with hist_col2:
                    st.markdown("**Literal Conversational Decoding Trace Output:**")
                    st.info(entry['result']['transcript'])
                    
                    st.markdown("**Acoustic Property Vectors:**")
                    st.json(entry['result']['metrics'])
                    
        if st.button("🗑️ Purge Analytics History Cache Logs", type="secondary", use_container_width=True):
            st.session_state.processing_history = []
            st.rerun()
    else:
        st.info("No system incident audit trails compiled in running session context arrays.")

with tab3:
    st.markdown("### 📖 System Engineering Documentation")
    doc_left, doc_right = st.columns(2)
    
    with doc_left:
        st.markdown("""
        #### 🎯 Project Scope Overview
        This terminal interface enables real-time visual interpretation of unstructured telecom support speech signals. It converts complex customer descriptions into high-detail context representations to optimize support ticket dispatching.
        
        #### ⚙️ Core Technology Architecture Stack
        - **ASR Engine Block**: Whisper Large-v3 Turbo for advanced transcription handling.
        - **Generative Graphics Synthesis Pipeline**: Stable Diffusion XL Base generating native 1024x1024 pixel photographic details.
        """)
        
    with doc_right:
        st.markdown("""
        #### 📊 Signal Analytics Specification Index
        - **RMS Loudness Matrix**: Represents energy fluctuations within the recording block.
        - **Spectral Centroid Profile**: Captures high-frequency distortions across line communication layers.
        - **Zero-Crossing Rate Factor**: Analyzes noisy vocal frequencies to parse speech context accurately.
        """)

# --- REPO BASE FOOTER BRANDING CARD ---
st.markdown("""
<div class="footer">
    <strong>Voice-to-Image Generation System v3.0</strong><br>
    SLT Mobitel Research Project Portfolio Pipeline | 2026<br>
    Intelligent Voice Understanding Platform for Telecom Customer Service<br>
    <em>ConnectPlus ISP Domain Architecture</em>
</div>
""", unsafe_allow_html=True)