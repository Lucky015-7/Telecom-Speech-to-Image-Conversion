import streamlit as st
import requests
import os

# --- PAGE INITIALIZATION ---
# Sets up the custom browser tab title and restricts the application display to a centered view layout
st.set_page_config(page_title="SLT Mobitel Generative Dashboard", layout="centered")

# --- INSTANCE CONFIGURATION ---
# Defines the backend base network address where the compute-heavy FastAPI instance runs locally
API_URL = "http://127.0.0.1:8000"

# --- USER INTERFACE STATIC HEADER ---
st.title("🎯 High-Accuracy Voice-to-Image Engine")
st.subheader("Telecom Customer Service Insights Console")
st.markdown("---")

# --- AUDIO FILE INGESTION COMPONENT ---
# Renders an interactive file drop-zone restricting uploads to standard voice recording container formats
uploaded_file = st.file_uploader("Upload Customer Incident Recording", type=["mpeg", "mp3", "wav"])

# --- CORE APPLICATION INFRASTRUCTURE BACKBONE ---
# Evaluates if a file asset has been mapped into memory via the uploader component
if uploaded_file is not None:
    # Renders an HTML5 media component interface for client-side recording playback assessment
    st.audio(uploaded_file, format="audio/mpeg")
    
    # Instantiates a primary action call button spanning across the entire horizontal column width
    trigger_generation = st.button("Generate Situational Image", type="primary", use_container_width=True)
    
    # Executes the server request transaction sequence when the client triggers the click event
    if trigger_generation:
        # Displays a synchronized loading ring container during compute-bound inference delays
        with st.spinner("Processing deep network pipeline stages... (This may take a moment to initialize)"):
            # Envelops raw file metadata and memory buffers into a standard HTTP multipart dictionary package
            multipart_payload = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            
            try:
                # Dispatches an HTTP POST network request forwarding the binary payload to the FastAPI core route
                response = requests.post(f"{API_URL}/api/v1/process-audio", files=multipart_payload)
                
                # Evaluates if the backend processing node completed the parsing sequence successfully
                if response.status_code == 200:
                    # Unpacks the returned JSON text mapping package back into a usable Python dictionary
                    payload = response.json()
                    
                    # Updates the user display interface with a successful status confirmation banner
                    st.success("Generative analysis sequence completed.")
                    
                    # --- STRUCTURAL METRIC BLOCKS LAYOUT ---
                    # Segments the page body area into three distinct tracking columns layout frames
                    m1, m2, m3 = st.columns(3)
                    # Maps companion acoustic diagnostic features directly onto clean numerical KPI block components
                    m1.metric("Signal RMS Loudness", payload['metrics']['energy'])
                    m2.metric("Spectral Tonal Brightness", payload['metrics']['brightness'])
                    m3.metric("Zero-Crossing Rate", payload['metrics']['zcr'])
                    
                    # --- TEXT OUTPUTS BOX DISPLAY ---
                    # Introduces section boundaries and outputs the full literal translation string extracted by Whisper
                    st.markdown("### 📋 Extracted Customer Complaint Transcript")
                    st.info(payload['transcript'])
                    
                    # --- FETCH AND RENDER FINAL GENERATION BLOB ASSET ---
                    # Constructs a parameterized network path pointing toward the newly created canvas image path location
                    image_request_url = f"{API_URL}/api/v1/fetch-image?path={payload['image_path']}"
                    # Executes an internal network call to fetch the static binary image file out from server storage paths
                    image_data = requests.get(image_request_url)
                    
                    # Verifies if the target high-resolution asset was recovered without communication drop-outs
                    if image_data.status_code == 200:
                        # Directs the static byte array to render into the active browser layout view
                        st.markdown("### 🖼️ High-Fidelity Synthesized Visual Output")
                        st.image(image_data.content, use_container_width=True, caption="Generated Scene Map Model Frame")
                    else:
                        # Notifies the client if the server system generated the data schema but failed to serve the physical file
                        st.error("Target asset stream could not be safely piped from backend processing nodes.")
                        
                else:
                    # Renders contextual execution framework error reports generated inside backend nodes
                    st.error(f"Backend Server Processing Error: {response.text}")
                    
            except Exception as connection_error:
                # Safely catches network timeouts or service offline states without crashing the running interface engine
                st.error(f"Could not connect to processing node backend server: {str(connection_error)}")