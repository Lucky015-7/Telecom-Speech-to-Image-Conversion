import streamlit as st
import requests
import os

st.set_page_config(page_title="SLT Mobitel Generative Dashboard", layout="centered")

API_URL = "http://127.0.0.1:8000"

st.title("🎯 High-Accuracy Voice-to-Image Engine")
st.subheader("Telecom Customer Service Insights Console")
st.markdown("---")

uploaded_file = st.file_uploader("Upload Customer Incident Recording", type=["mpeg", "mp3", "wav"])

if uploaded_file is not None:
    # Render native client playback widget
    st.audio(uploaded_file, format="audio/mpeg")
    
    trigger_generation = st.button("Generate Situational Image", type="primary", use_container_width=True)
    
    if trigger_generation:
        with st.spinner("Processing deep network pipeline stages... (This may take a moment to initialize)"):
            # Construct standard multipart form transfer envelope packages
            multipart_payload = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            
            try:
                response = requests.post(f"{API_URL}/api/v1/process-audio", files=multipart_payload)
                
                if response.status_code == 200:
                    payload = response.json()
                    
                    st.success("Generative analysis sequence completed.")
                    
                    # --- Structural Metric Blocks Layout ---
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Signal RMS Loudness", payload['metrics']['energy'])
                    m2.metric("Spectral Tonal Brightness", payload['metrics']['brightness'])
                    m3.metric("Zero-Crossing Rate", payload['metrics']['zcr'])
                    
                    # --- Text Outputs Box Display ---
                    st.markdown("### 📋 Extracted Customer Complaint Transcript")
                    st.info(payload['transcript'])
                    
                    # --- Fetch and Render Final Generation Blob Asset ---
                    image_request_url = f"{API_URL}/api/v1/fetch-image?path={payload['image_path']}"
                    image_data = requests.get(image_request_url)
                    
                    if image_data.status_code == 200:
                        st.markdown("### 🖼️ High-Fidelity Synthesized Visual Output")
                        st.image(image_data.content, use_container_width=True, caption="Generated Scene Map Model Frame")
                    else:
                        st.error("Target asset stream could not be safely piped from backend processing nodes.")
                        
                else:
                    st.error(f"Backend Server Processing Error: {response.text}")
                    
            except Exception as connection_error:
                st.error(f"Could not connect to processing node backend server: {str(connection_error)}")