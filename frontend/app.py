"""
SLT Mobitel Generative Dashboard - Frontend Client Application
==============================================================
This is a Streamlit-based user interface that acts as the frontend console for the 
High-Accuracy Voice-to-Image Engine. It allows telecom operators to upload customer 
incident voice recordings, send them to a backend processing pipeline, and visualize 
real-time analytical metrics, transcribed text, and a synthesized visual scene of the incident.

Pipeline Flow:
1. User uploads a customer incident audio recording (mp3, wav, mpeg).
2. The client plays back the audio using native Streamlit audio widgets.
3. Upon triggering generation, the audio is sent to the backend endpoint (/api/v1/process-audio).
4. The backend returns extracted audio features (energy, brightness, zcr), the complaint transcript, and an image path.
5. The frontend displays the metrics, transcript, and fetches the synthesized image via (/api/v1/fetch-image).
"""

import streamlit as st
import requests
import os

# --- Page Configurations & Theme Setup ---
# Set the page title and center the layout for a premium dashboard look and feel
st.set_page_config(page_title="SLT Mobitel Generative Dashboard", layout="centered")

# Base URL of the backend API service (FastAPI backend running locally)
API_URL = "http://127.0.0.1:8000"

# --- UI Header Section ---
st.title("🎯 High-Accuracy Voice-to-Image Engine")
st.subheader("Telecom Customer Service Insights Console")
st.markdown("---")

# --- Audio Upload Section ---
# Allow operators to upload customer call recordings (supporting standard audio formats)
uploaded_file = st.file_uploader("Upload Customer Incident Recording", type=["mpeg", "mp3", "wav"])

if uploaded_file is not None:
    # Render native client playback widget so the operator can listen to the recording
    st.audio(uploaded_file, format="audio/mpeg")
    
    # Primary CTA button to kick off the AI processing pipeline
    trigger_generation = st.button("Generate Situational Image", type="primary", use_container_width=True)
    
    if trigger_generation:
        # Show a loading spinner during network request and backend computation
        with st.spinner("Processing deep network pipeline stages... (This may take a moment to initialize)"):
            # Construct standard multipart form transfer envelope packages to send the raw file bytes
            multipart_payload = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            
            try:
                # STEP 1: POST the audio file to the backend to transcribe and extract features/metadata
                response = requests.post(f"{API_URL}/api/v1/process-audio", files=multipart_payload)
                
                if response.status_code == 200:
                    payload = response.json()
                    
                    st.success("Generative analysis sequence completed.")
                    
                    # --- Structural Metric Blocks Layout ---
                    # Display extracted audio features (Signal RMS, Spectral Tonal Brightness, Zero-Crossing Rate) in columns
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Signal RMS Loudness", payload['metrics']['energy'])
                    m2.metric("Spectral Tonal Brightness", payload['metrics']['brightness'])
                    m3.metric("Zero-Crossing Rate", payload['metrics']['zcr'])
                    
                    # --- Text Outputs Box Display ---
                    # Render the transcribed text of the customer's complaint using an info alert block
                    st.markdown("### 📋 Extracted Customer Complaint Transcript")
                    st.info(payload['transcript'])
                    
                    # --- Fetch and Render Final Generation Blob Asset ---
                    # STEP 2: Use the image path returned from the previous step to request the actual image file bytes
                    image_request_url = f"{API_URL}/api/v1/fetch-image?path={payload['image_path']}"
                    image_data = requests.get(image_request_url)
                    
                    if image_data.status_code == 200:
                        st.markdown("### 🖼️ High-Fidelity Synthesized Visual Output")
                        # Display the image stream received from the backend with standard layout formatting
                        st.image(image_data.content, use_container_width=True, caption="Generated Scene Map Model Frame")
                    else:
                        st.error("Target asset stream could not be safely piped from backend processing nodes.")
                        
                else:
                    st.error(f"Backend Server Processing Error: {response.text}")
                    
            except Exception as connection_error:
                # Handle networking errors, e.g. when backend is offline or unreachable
                st.error(f"Could not connect to processing node backend server: {str(connection_error)}")