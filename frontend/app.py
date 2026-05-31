import streamlit as st
import requests
import os
from datetime import datetime

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SLT Mobitel Generative Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* Background */
    .stApp {
        background: radial-gradient(ellipse at 20% 20%, #0d1b2a 0%, #0a0a12 50%, #100d1f 100%);
        background-attachment: fixed;
    }

    /* Noise overlay */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
        pointer-events: none;
        z-index: 0;
        opacity: 0.4;
    }

    /* Header */
    .hero-header {
        background: linear-gradient(135deg, #0d1b2a 0%, #162032 60%, #1a1230 100%);
        border: 1px solid rgba(56, 189, 248, 0.15);
        border-radius: 20px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 40px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.05);
    }

    .hero-header::after {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(56,189,248,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }

    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: 2.6rem;
        font-weight: 800;
        color: #f0f9ff;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }

    .hero-title span {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #7dd3fc;
        font-weight: 300;
        margin: 0;
        letter-spacing: 0.5px;
    }

    /* Upload area */
    .upload-wrap {
        background: linear-gradient(135deg, #0f1f30 0%, #131b28 100%);
        border: 2px dashed rgba(56,189,248,0.25);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: border-color 0.3s;
    }

    .upload-wrap:hover {
        border-color: rgba(56,189,248,0.5);
    }

    /* File info card */
    .file-card {
        background: linear-gradient(135deg, #0f1f30, #162032);
        border-left: 4px solid #38bdf8;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        color: #e0f2fe;
        font-size: 0.9rem;
        line-height: 1.8;
    }

    .file-card strong { color: #7dd3fc; }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #0d1b2a, #162032);
        border: 1px solid rgba(56,189,248,0.15);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        transition: transform 0.25s, box-shadow 0.25s;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 36px rgba(56,189,248,0.15);
        border-color: rgba(56,189,248,0.35);
    }

    .metric-value {
        font-family: 'Syne', sans-serif;
        font-size: 1.9rem;
        font-weight: 700;
        color: #38bdf8;
        margin: 0.4rem 0;
    }

    .metric-label {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 500;
    }

    .metric-sub {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 0.3rem;
    }

    /* Section panels */
    .panel {
        background: linear-gradient(135deg, #0f1f30, #131b28);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin: 1.5rem 0;
    }

    .panel-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #e0f2fe;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Info / success / result boxes */
    .info-box {
        background: rgba(14,165,233,0.07);
        border-left: 4px solid #38bdf8;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        color: #e0f2fe;
        font-size: 1rem;
        line-height: 1.7;
        margin: 0.8rem 0;
    }

    .success-box {
        background: rgba(16,185,129,0.08);
        border-left: 4px solid #10b981;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        color: #d1fae5;
        margin: 1rem 0;
    }

    .success-box h4 { color: #34d399; margin: 0 0 0.3rem 0; font-family: 'Syne', sans-serif; }
    .success-box p  { margin: 0; font-size: 0.9rem; color: #a7f3d0; }

    /* Category badge */
    .category-badge {
        display: inline-block;
        background: linear-gradient(90deg, #1e3a5f, #1e2d50);
        border: 1px solid #38bdf8;
        color: #7dd3fc;
        font-family: 'Syne', sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        padding: 0.5rem 1.2rem;
        border-radius: 30px;
        letter-spacing: 0.5px;
    }

    /* History item */
    .history-item {
        background: linear-gradient(135deg, #0d1b2a, #162032);
        border: 1px solid rgba(56,189,248,0.1);
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        transition: border-color 0.2s;
    }

    .history-item:hover { border-color: rgba(56,189,248,0.3); }

    .history-item p {
        margin: 0.2rem 0;
        color: #cbd5e1;
        font-size: 0.9rem;
    }

    .history-item strong { color: #7dd3fc; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0369a1, #0ea5e9) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 1.8rem !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 6px 20px rgba(14,165,233,0.3) !important;
        transition: all 0.25s !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 28px rgba(14,165,233,0.45) !important;
        background: linear-gradient(135deg, #0284c7, #38bdf8) !important;
    }

    /* Welcome card */
    .welcome-card {
        text-align: center;
        padding: 3.5rem 2rem;
        background: linear-gradient(135deg, #0d1b2a, #131b28);
        border: 1px dashed rgba(56,189,248,0.2);
        border-radius: 20px;
        margin: 2rem 0;
    }

    .welcome-card h2 {
        font-family: 'Syne', sans-serif;
        font-size: 1.9rem;
        font-weight: 700;
        color: #f0f9ff;
        margin-bottom: 0.8rem;
    }

    .welcome-card p { color: #94a3b8; font-size: 0.95rem; margin: 0.4rem 0; }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #0d1b2a, #131b28);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        margin-top: 2rem;
    }

    .footer h4 { font-family: 'Syne', sans-serif; color: #38bdf8; margin-bottom: 0.5rem; }
    .footer p  { color: #64748b; font-size: 0.85rem; margin: 0; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #080e17 0%, #0d1b2a 100%);
        border-right: 1px solid rgba(56,189,248,0.1);
    }

    section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }

    /* Dividers */
    hr { border-color: rgba(255,255,255,0.06) !important; }

    /* Headings inside markdown */
    h1, h2, h3, h4, h5, h6 { color: #f0f9ff !important; font-family: 'Syne', sans-serif !important; }

    /* Hide Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer     { visibility: hidden; }

    /* Spinner text */
    .stSpinner > div { border-top-color: #38bdf8 !important; }
</style>
""", unsafe_allow_html=True)

# ── Configuration Settings ────────────────────────────────────────────────────────────────────
# Define the local host URL where the FastAPI backend microservice is listening

API_URL = "http://127.0.0.1:8000"

# ── Sidebar Panel Layout───────────────────────────────────────────────────────────────────
# Construct an interactive navigation and technical metadata panel in the sidebar

with st.sidebar:
    st.markdown("## 🎯 SLT Mobitel")
    st.markdown("**Generative Dashboard**")
    st.markdown("---")

     # Display the list of core platform capabilities
    st.markdown("#### ⚡ Features")
    st.markdown("""
- Voice Transcription (Whisper AI)
- Acoustic Analysis (Librosa)
- AI Image Generation (Stable Diffusion)
- Issue Categorization
- Generation History
- Category Analytics
    """)

    st.markdown("---")

    # List all supported audio formats accepted by both frontend & backend uploaders
    st.markdown("#### 🎵 Supported Formats")
    st.markdown("""
- MPEG Audio (.mpeg)
- MP3 Files (.mp3)
- WAV Files (.wav)
- M4A Files (.m4a)
- WebM Audio (.webm)
- OGG Files (.ogg)
    """)

    st.markdown("---")

    # Provide brief context about the application's underlying architecture
    st.markdown("#### ℹ️ About")
    st.markdown("""
Advanced AI-powered platform for converting telecom customer voice recordings into visual representations using state-of-the-art deep learning.
    """)

    st.markdown("---")
    st.caption(f"© {datetime.now().year} SLT Mobitel AI Platform")
    st.caption(f"{datetime.now().strftime('%B %d, %Y')}")

# ── Hero Header ───────────────────────────────────────────────────────────────
# Renders a sleek, modern glassmorphic header block with soft neon highlights

st.markdown("""
<div class='hero-header'>
    <p class='hero-title'>🎯 High-Accuracy <span>Voice-to-Image</span> Engine</p>
    <p class='hero-subtitle'>Telecom Customer Service Insights Console — Powered by Whisper · Stable Diffusion · Librosa</p>
</div>
""", unsafe_allow_html=True)

# ── File Upload Widget ────────────────────────────────────────────────────────────
# Displays a styled upload boundary card

st.markdown("""
<div class='upload-wrap'>
    <h4 style='color:#7dd3fc; text-align:center; margin:0 0 0.5rem 0; font-family:Syne,sans-serif;'>
        📁 Upload Customer Incident Recording
    </h4>
    <p style='color:#64748b; text-align:center; font-size:0.85rem; margin:0;'>
        Supports MPEG · MP3 · WAV · M4A · WebM · OGG
    </p>
</div>
""", unsafe_allow_html=True)

# Streamlit file upload boundary widget supporting audio files
uploaded_file = st.file_uploader(
    "Choose an audio file",
    type=["mpeg", "mp3", "wav", "m4a", "webm", "ogg"],
    help="Upload a customer incident recording for AI analysis"
)

# ── Main Generation & Operations Logic ────────────────────────────────────────────────────────────────
# Triggered only when a file has been successfully uploaded into memory

if uploaded_file is not None:

 # File Details Card: Displays name, file size (in KB), and mime-type
    st.markdown(f"""
    <div class='file-card'>
        <strong>📄 File:</strong> {uploaded_file.name}&nbsp;&nbsp;
        <strong>📦 Size:</strong> {uploaded_file.size / 1024:.2f} KB&nbsp;&nbsp;
        <strong>🎙️ Type:</strong> {uploaded_file.type}
    </div>
    """, unsafe_allow_html=True)

    # Audio Playback Player: Native preview player to listen to the uploaded incident recording
    st.markdown("<h4 style='color:#7dd3fc;'>🔊 Audio Preview</h4>", unsafe_allow_html=True)
    st.audio(uploaded_file, format=uploaded_file.type)

    st.markdown("<br>", unsafe_allow_html=True)

# Centered Primary CTA Button to trigger the deep learning pipeline
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        trigger_generation = st.button(
            "🚀 Generate Situational Image",
            type="primary",
            use_container_width=True
        )

    #  ── Pipeline Execution  ────────────────────────────────────────────────────────────
    # Triggered upon clicking the generation button
        
        if trigger_generation:
        with st.spinner("Processing deep network pipeline stages… (This may take a moment)"):
            progress_bar = st.progress(0)
            progress_bar.progress(20)

    # Build a multipart/form-data payload containing raw audio file bytes
            multipart_payload = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            try:
                progress_bar.progress(45)
  # Send the multipart request to the FastAPI backend's process-audio route
                response = requests.post(
                    f"{API_URL}/api/v1/process-audio",
                    files=multipart_payload
                )
                progress_bar.progress(75)
 # If connection and processing are successful, unpack results
                if response.status_code == 200:
                    payload = response.json()
                    progress_bar.progress(100)

# Unpack the nested "result" document matching backend schemas
                    result    = payload.get("result", {})
                    result_id = result.get("_id")
                    transcript = result.get("transcript", "No transcript available")
                    metrics    = result.get("metrics", {})
                    category   = result.get("category", "unknown")
                    prompt     = result.get("prompt", "No prompt available")
                    
 # Display success notification
                    st.markdown("""
                    <div class='success-box'>
                        <h4>✅ Generative Analysis Complete!</h4>
                        <p>Your audio has been successfully processed through the AI pipeline.</p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    
 # ── Render Acoustic Diagnostics Cards 
 # Displays Librosa-calculated waveform features inside premium interactive cards
                    st.markdown("<h3 style='color:#38bdf8; text-align:center;'>📡 Acoustic Analysis Metrics</h3>", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

                    m1, m2, m3 = st.columns(3)
# Card 1: Signal RMS Loudness (Energy Level)
                    with m1:
                        st.markdown(f"""
                        <div class='metric-card'>
                            <div class='metric-label'>Signal RMS Loudness</div>
                            <div class='metric-value'>{metrics.get("rms_energy", metrics.get("energy", 0))}</div>
                            <div class='metric-sub'>Energy Level</div>
                        </div>
                        """, unsafe_allow_html=True)
 # Card 2: Spectral Tonal Brightness (Tonal Quality)
                    with m2:
                        st.markdown(f"""
                        <div class='metric-card'>
                            <div class='metric-label'>Spectral Tonal Brightness</div>
                            <div class='metric-value'>{metrics.get("brightness", 0)}</div>
                            <div class='metric-sub'>Tonal Quality</div>
                        </div>
                        """, unsafe_allow_html=True)
 # Card 3: Zero-Crossing Rate (Frequency Analysis)
                    with m3:
                        st.markdown(f"""
                        <div class='metric-card'>
                            <div class='metric-label'>Zero-Crossing Rate</div>
                            <div class='metric-value'>{metrics.get("zero_crossing_rate", metrics.get("zcr", 0))}</div>
                            <div class='metric-sub'>Frequency Analysis</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

     # ── Render Telecom Issue Category 
     # Displays the category badge parsed by the vocab rules
                    st.markdown("""
                    <div class='panel'>
                        <div class='panel-title'>🧠 Telecom Issue Category</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"<div style='margin-top:-1rem; padding:0 0.5rem;'><span class='category-badge'>{category}</span></div>", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
# ── Render ASR Complaint Transcript 
# Displays the text transcribed by the Whisper engine
                   
                    st.markdown("""
                    <div class='panel'>
                        <div class='panel-title'>📋 Extracted Customer Complaint Transcript</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"<div class='info-box' style='margin-top:-1rem;'>{transcript}</div>", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

        # ── Render Image Generation Prompt 
        # Displays the detailed visual prompt built by the vocabulary layer
                    st.markdown("""
                    <div class='panel'>
                        <div class='panel-title'>📝 Generated Image Prompt</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"<div class='info-box' style='margin-top:-1rem;'>{prompt}</div>", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

         # ── Render Final Synthesized Image ────────────────────────
         # Securely requests the generated PNG from the backend using the database result ID
                    if result_id:
                        image_request_url = f"{API_URL}/api/v1/fetch-image/{result_id}"
                        image_data = requests.get(image_request_url)

         # If download is successful, render the centered visual output

                        if image_data.status_code == 200:
                            st.markdown("<h3 style='color:#38bdf8;'>🖼️ High-Fidelity Synthesized Visual Output</h3>", unsafe_allow_html=True)
                            col1, col2, col3 = st.columns([1, 4, 1])
                            with col2:
                                st.image(
                                    image_data.content,
                                    use_container_width=True,
                                    caption="Generated Scene Map Model Frame — Stable Diffusion"
                                )
                        else:
                            st.error("❌ Target asset stream could not be safely piped from backend processing nodes.")
                    else:
                        st.error("❌ Result ID was not returned by backend. Cannot fetch generated image.")

                else:
                    st.error(f"❌ Backend Server Processing Error: {response.text}")

            except Exception as connection_error:
                st.error(f"❌ Could not connect to processing node backend server: {str(connection_error)}")

else:
     # ── Onboarding Welcome Screen 
    # Renders an introductory guide with dynamic tech stack highlights when no file is uploaded
    st.markdown("""
    <div class='welcome-card'>
        <h2>👋 Welcome to the Voice-to-Image AI Platform</h2>
        <p>Upload a customer incident recording above to begin AI-powered analysis and visualization.</p>
        <p>Our models will transcribe the audio, analyze acoustic features, categorize the issue,<br>and generate a visual representation of the incident.</p>
        <br>
        <p style='color:#38bdf8; font-size:0.85rem; letter-spacing:1px;'>WHISPER AI &nbsp;·&nbsp; STABLE DIFFUSION &nbsp;·&nbsp; LIBROSA &nbsp;·&nbsp; FASTAPI &nbsp;·&nbsp; MONGODB</p>
    </div>
    """, unsafe_allow_html=True)

# ── Operations History Section 
# Displays persistent past complaints and generated pictures from database queries
st.markdown("---")
st.markdown("<h3>📂 Recent Backend Generation History</h3>", unsafe_allow_html=True)

# Operator triggers database query upon clicking
if st.button("Load Recent Results"):
    try:

# Request all recent generation results from the backend audit API
    
        history_response = requests.get(f"{API_URL}/api/v1/results")

        if history_response.status_code == 200:
            history_payload = history_response.json()
            results = history_payload.get("results", [])

            if len(results) == 0:
                st.info("No previous generation records found.")
            else:

    # Loop through database transactions and render descriptive cards + images
                for item in results:
                    st.markdown(f"""
                    <div class='history-item'>
                        <p><strong>🆔 Result ID:</strong> {item.get('_id')}</p>
                        <p><strong>📄 Original File:</strong> {item.get('original_filename')}</p>
                        <p><strong>⚙️ Status:</strong> {item.get('status')}</p>
                        <p><strong>🧠 Category:</strong> {item.get('category')}</p>
                        <p><strong>📋 Transcript:</strong> {item.get('transcript')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    item_id = item.get("_id")
                    if item_id:

          # Fetch the static PNG bytes from the secure fetch image endpoint
                        image_url = f"{API_URL}/api/v1/fetch-image/{item_id}"
                        image_response = requests.get(image_url)

                        if image_response.status_code == 200:
                            st.image(
                                image_response.content,
                                use_container_width=True,
                                caption=f"Generated Image — {item.get('category')}"
                            )
        else:
            st.error(f"❌ Could not load result history: {history_response.text}")

    except Exception as history_error:
        st.error(f"❌ Could not connect to backend history endpoint: {str(history_error)}")

# ── Incident Analytics Section 
# Displays a data matrix of complaint category distributions aggregated by MongoDB
st.markdown("---")
st.markdown("<h3>📊 Backend Analytics</h3>", unsafe_allow_html=True)

if st.button("Load Category Analytics"):
    try:

 # Request the category aggregation results from the analytics API
        analytics_response = requests.get(f"{API_URL}/api/v1/analytics/categories")

        if analytics_response.status_code == 200:
            analytics_payload = analytics_response.json()
            analytics = analytics_payload.get("analytics", [])

            if len(analytics) == 0:
                st.info("No analytics data available yet.")
            else:

        # Render the returned counts as a structured Streamlit table
                st.table(analytics)
        else:
            st.error(f"❌ Could not load analytics: {analytics_response.text}")

    except Exception as analytics_error:
        st.error(f"❌ Could not connect to backend analytics endpoint: {str(analytics_error)}")

# ── Project Brand Footer 
# Premium developer signature signature block at the bottom of the viewport
st.markdown("""
<div class='footer'>
    <h4>⚡ Powered by Advanced AI Technology</h4>
    <p>Whisper AI &nbsp;·&nbsp; Stable Diffusion &nbsp;·&nbsp; Librosa &nbsp;·&nbsp; FastAPI &nbsp;·&nbsp; MongoDB</p>
</div>
""", unsafe_allow_html=True)
