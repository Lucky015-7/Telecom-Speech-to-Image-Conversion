"""
Streamlit Frontend for Voice-to-Image Generation System
SLT Mobitel Research Project
"""

import streamlit as st
import requests
from PIL import Image
import io
import time
from pathlib import Path
import json

# Page configuration
st.set_page_config(
    page_title="Voice-to-Image | SLT Mobitel",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for attractive styling
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

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Initialize session state
if 'processing_history' not in st.session_state:
    st.session_state.processing_history = []

def check_api_health():
    """Check if backend API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def process_audio(audio_file, mode):
    """Send audio to backend for processing"""
    endpoint = f"{API_BASE_URL}/process/mode-{mode.lower()}"
    
    files = {"file": (audio_file.name, audio_file, audio_file.type)}
    
    try:
        response = requests.post(endpoint, files=files, timeout=300)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def get_image(filename):
    """Retrieve generated image from backend"""
    try:
        response = requests.get(f"{API_BASE_URL}/image/{filename}", timeout=30)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content))
    except:
        return None

# Header
st.markdown("""
<div class="main-header">
    <h1>🎙️ Voice-to-Image Generation System</h1>
    <p>Intelligent Voice Understanding Platform for Telecom Customer Service</p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">
        <strong>SLT Mobitel Research Project</strong> | ConnectPlus ISP Domain
    </p>
</div>
""", unsafe_allow_html=True)

# Check API status
api_status = check_api_health()

if not api_status:
    st.error("⚠️ Backend API is not running. Please start the backend server first.")
    st.code("python -m uvicorn backend.main:app --reload", language="bash")
    st.stop()

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/E31837/FFFFFF?text=SLT+Mobitel", use_container_width=True)
    
    st.markdown("### 🎯 Processing Mode")
    
    mode = st.radio(
        "Select AI Processing Mode:",
        options=["A", "B"],
        format_func=lambda x: {
            "A": "🔊 Mode A: Audio-Direct Retrieval",
            "B": "🗣️ Mode B: Speech Recognition"
        }[x],
        help="Choose how the system should process your audio"
    )
    
    st.markdown("---")
    
    # Mode information
    if mode == "A":
        st.markdown("""
        <div class="info-card">
            <h4>🔊 Mode A: Audio-Direct</h4>
            <p><strong>Technology:</strong> CLAP Audio Embedding</p>
            <p><strong>Best for:</strong> Noisy or unclear audio</p>
            <p><strong>Process:</strong> Text-free acoustic analysis</p>
            <span class="feature-badge">Fast</span>
            <span class="feature-badge">Robust</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-card">
            <h4>🗣️ Mode B: Speech-Guided</h4>
            <p><strong>Technology:</strong> Whisper ASR + Stable Diffusion</p>
            <p><strong>Best for:</strong> Clear, articulate speech</p>
            <p><strong>Process:</strong> Speech-to-text-to-image</p>
            <span class="feature-badge">Accurate</span>
            <span class="feature-badge">Detailed</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 System Info")
    st.info(f"✅ API Status: **Online**\n\n🖥️ Backend: **Ready**\n\n🤖 Models: **Loaded**")
    
    st.markdown("---")
    
    st.markdown("### 📚 About")
    st.markdown("""
    This system translates spoken audio from telecom customer service 
    interactions into contextually relevant images using state-of-the-art AI.
    
    **Supported Scenarios:**
    - 🌐 Internet connectivity issues
    - 📺 Television service problems
    - 🔧 Field technician operations
    """)

# Main content area
tab1, tab2, tab3 = st.tabs(["🎙️ Process Audio", "📊 Results Dashboard", "ℹ️ Documentation"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Upload Audio File")
        
        audio_file = st.file_uploader(
            "Choose a voice recording",
            type=["mp3", "wav", "mpeg", "m4a", "flac"],
            help="Upload a customer service voice recording"
        )
        
        if audio_file:
            st.audio(audio_file, format=f"audio/{audio_file.type.split('/')[-1]}")
            
            st.markdown(f"""
            <div class="info-card">
                <strong>📁 File:</strong> {audio_file.name}<br>
                <strong>📏 Size:</strong> {audio_file.size / 1024:.2f} KB<br>
                <strong>🎵 Type:</strong> {audio_file.type}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Generate Image", type="primary"):
                with st.spinner(f"🔄 Processing with Mode {mode}... This may take 30-60 seconds..."):
                    # Progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("📥 Uploading audio file...")
                    progress_bar.progress(20)
                    time.sleep(0.5)
                    
                    if mode == "A":
                        status_text.text("🔊 Encoding audio with CLAP...")
                        progress_bar.progress(40)
                    else:
                        status_text.text("🗣️ Transcribing with Whisper...")
                        progress_bar.progress(40)
                    
                    # Process audio
                    result = process_audio(audio_file, mode)
                    
                    if result and result.get('success'):
                        status_text.text("🎨 Generating image with Stable Diffusion...")
                        progress_bar.progress(70)
                        time.sleep(0.5)
                        
                        status_text.text("✅ Finalizing...")
                        progress_bar.progress(100)
                        
                        # Store in session state
                        st.session_state.current_result = result
                        st.session_state.processing_history.append({
                            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                            'mode': mode,
                            'filename': audio_file.name,
                            'result': result
                        })
                        
                        st.success("✅ Image generated successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Processing failed. Please try again.")
                        progress_bar.empty()
                        status_text.empty()
    
    with col2:
        st.markdown("### 🖼️ Generated Image")
        
        if 'current_result' in st.session_state:
            result = st.session_state.current_result
            
            # Get and display image
            image = get_image(result['output_image'])
            
            if image:
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(image, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Download button
                img_buffer = io.BytesIO()
                image.save(img_buffer, format='PNG')
                st.download_button(
                    label="💾 Download Image",
                    data=img_buffer.getvalue(),
                    file_name=result['output_image'],
                    mime="image/png"
                )
            
            # Display results
            st.markdown("### 📈 Analysis Results")
            
            # Metrics
            metric_cols = st.columns(3)
            
            with metric_cols[0]:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{result.get('clip_score', 0):.3f}</div>
                    <div class="metric-label">CLIP Score</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[1]:
                duration = result.get('acoustic_features', {}).get('duration', 0)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{duration:.1f}s</div>
                    <div class="metric-label">Audio Duration</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[2]:
                energy = result.get('acoustic_features', {}).get('energy', 0)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{energy:.3f}</div>
                    <div class="metric-label">Audio Energy</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Mode-specific information
            if result['mode'] == 'A':
                st.markdown("#### 🎯 Matched Scene")
                st.info(f"**{result['matched_scene']}**")
                st.metric("Similarity Score", f"{result['similarity_score']:.3f}")
                
                with st.expander("🔍 View Top 5 Matches"):
                    for i, match in enumerate(result.get('top_matches', []), 1):
                        st.write(f"{i}. {match['scene']} - Score: {match['score']:.3f}")
            
            else:  # Mode B
                st.markdown("#### 📝 Transcript")
                st.info(result['transcript'])
            
            # Acoustic features
            with st.expander("🎵 Acoustic Features"):
                features = result.get('acoustic_features', {})
                st.json(features)
        
        else:
            st.info("👆 Upload an audio file and click 'Generate Image' to see results here.")

with tab2:
    st.markdown("### 📊 Processing History")
    
    if st.session_state.processing_history:
        for i, entry in enumerate(reversed(st.session_state.processing_history), 1):
            with st.expander(f"🕐 {entry['timestamp']} - {entry['filename']} (Mode {entry['mode']})"):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    image = get_image(entry['result']['output_image'])
                    if image:
                        st.image(image, use_container_width=True)
                
                with col2:
                    st.metric("CLIP Score", f"{entry['result'].get('clip_score', 0):.3f}")
                    
                    if entry['mode'] == 'A':
                        st.write("**Matched Scene:**")
                        st.write(entry['result']['matched_scene'])
                    else:
                        st.write("**Transcript:**")
                        st.write(entry['result']['transcript'])
        
        if st.button("🗑️ Clear History"):
            st.session_state.processing_history = []
            st.rerun()
    else:
        st.info("No processing history yet. Process some audio files to see results here.")

with tab3:
    st.markdown("### 📖 System Documentation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🎯 Project Overview
        
        The **Voice-to-Image Generation System** is a research prototype developed 
        for SLT Mobitel that translates spoken audio from telecom customer service 
        interactions into contextually relevant images.
        
        #### 🔬 Technology Stack
        
        - **Whisper**: Automatic Speech Recognition
        - **CLAP**: Audio-Language Embedding
        - **Stable Diffusion**: Text-to-Image Generation
        - **CLIP**: Image-Text Similarity Evaluation
        
        #### 🎨 Processing Modes
        
        **Mode A: Audio-Direct Retrieval**
        - Uses CLAP audio embeddings
        - Text-free processing
        - Best for noisy audio
        - Matches against 66 pre-defined scenes
        
        **Mode B: Speech Recognition**
        - Uses Whisper ASR + Stable Diffusion
        - Converts speech to text to image
        - Best for clear speech
        - Open-ended generation
        """)
    
    with col2:
        st.markdown("""
        #### 🏢 Domain Coverage
        
        **ConnectPlus ISP Service Areas:**
        
        1. **Internet Connectivity** 🌐
           - Router problems
           - Network outages
           - Slow speeds
        
        2. **Television Services** 📺
           - No signal issues
           - Set-top box faults
           - Broadcast problems
        
        3. **Field Operations** 🔧
           - Tower damage
           - Cable faults
           - Technician visits
        
        #### 📊 Evaluation Metrics
        
        - **CLIP Similarity Score**: Measures image-text alignment
        - **Acoustic Features**: Energy, brightness, zero-crossing rate
        - **Processing Time**: End-to-end generation time
        
        #### 👥 Credits
        
        **Organization**: SLT Mobitel Research  
        **Domain**: Artificial Intelligence / NLP  
        **Version**: 3.0 (2026)  
        **Status**: Research Prototype
        """)

# Footer
st.markdown("""
<div class="footer">
    <strong>Voice-to-Image Generation System v3.0</strong><br>
    SLT Mobitel Research Project | 2026<br>
    Intelligent Voice Understanding Platform for Telecom Customer Service<br>
    <em>ConnectPlus ISP Domain</em>
</div>
""", unsafe_allow_html=True)
