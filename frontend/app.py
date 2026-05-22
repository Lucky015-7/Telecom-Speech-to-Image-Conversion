import streamlit as st
import requests
import os

# --- PAGE CONFIGURATION ---
# Configures the global web browser page tab title and forces the UI layout to wrap in a centered view
st.set_page_config(
    page_title="SLT Mobitel Generative Dashboard", layout="centered")

# --- BACKEND LINKAGE CONSTANTS ---
# Defines the core base network address where the background compute-bound FastAPI instance is bound
API_URL = "http://127.0.0.1:8000"

# --- USER INTERFACE HEADER BLOCK ---
st.title("🎯 High-Accuracy Voice-to-Image Engine")
st.subheader("Telecom Customer Service Insights Console")
st.markdown("---")

# --- FILE UPLOADER COMPONENT ---
# Renders an interactive drag-and-drop landing field that accepts target voice recording formats
uploaded_file = st.file_uploader(
    "Upload Customer Incident Recording", type=["mpeg", "mp3", "wav"])

# --- CORE APPLICATION LOGIC BINDING ---
# Evaluates if a customer voice file asset has been successfully dropped or parsed into memory
if uploaded_file is not None:

    # Renders a standard HTML5 native audio controller interface for client-side recording playback
    st.audio(uploaded_file, format="audio/mpeg")

    # Renders an highlighted primary action button stretched across the width of the page column
    trigger_generation = st.button(
        "Generate Situational Image", type="primary", use_container_width=True)

    # Triggers the processing stream when the client fires the generation button click event
    if trigger_generation:

        # Displays a synchronized loading spinner block to keep the UI responsive during deep learning inference
        with st.spinner("Processing deep network pipeline stages... (This may take a moment to initialize)"):

            # Encapsulates raw file bytes into a standard multi-part boundary stream payload for network transport
            multipart_payload = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

            try:
                # Dispatches an asynchronous HTTP POST request driving data packets directly into the FastAPI core routing cluster
                response = requests.post(
                    f"{API_URL}/api/v1/process-audio", files=multipart_payload)

                # Evaluates if the computing backend completed the inference transaction successfully
                if response.status_code == 200:
                    # Unpacks JSON text dictionaries returned from backend pipelines into a usable Python dictionary
                    payload = response.json()

                    # Updates UI with a positive feedback status alert block
                    st.success("Generative analysis sequence completed.")

                    # --- STRUCTURAL METRIC BLOCKS LAYOUT ---
                    # Splits the horizontal workspace area into 3 distinct fluid metadata tracking blocks
                    m1, m2, m3 = st.columns(3)

                    # Maps companion acoustic telemetric data fields onto high-visibility KPI indicator display nodes
                    m1.metric("Signal RMS Loudness",
                              payload['metrics']['energy'])
                    m2.metric("Spectral Tonal Brightness",
                              payload['metrics']['brightness'])
                    m3.metric("Zero-Crossing Rate", payload['metrics']['zcr'])

                    # --- TEXT OUTPUTS BOX DISPLAY ---
                    # Displays a markdown section header and embeds the verbatim text transcript returned from Whisper
                    st.markdown(
                        "### 📋 Extracted Customer Complaint Transcript")
                    st.info(payload['transcript'])

                    # --- FETCH AND RENDER FINAL GENERATION BLOB ASSET ---
                    # Constructs a parameterized GET resource URL pointing to the location of the newly generated image path
                    image_request_url = f"{API_URL}/api/v1/fetch-image?path={payload['image_path']}"

                    # Dispatches a request to read the file-system binary image stream back over HTTP
                    image_data = requests.get(image_request_url)

                    # Validates that the file blob was recovered from storage paths without errors
                    if image_data.status_code == 200:
                        # Renders the raw image matrix directly onto the browser layout window frame
                        st.markdown(
                            "### 🖼️ High-Fidelity Synthesized Visual Output")
                        st.image(image_data.content, use_container_width=True,
                                 caption="Generated Scene Map Model Frame")
                    else:
                        # Fires a failure alert if the specific generated image path cannot be read or retrieved
                        st.error(
                            "Target asset stream could not be safely piped from backend processing nodes.")

                else:
                    # Renders a contextual server framework error state block showing returned error details
                    st.error(
                        f"Backend Server Processing Error: {response.text}")

            except Exception as connection_error:
                # Handles hardware network timeouts or server offline failure states safely without breaking the browser frame
                st.error(
                    f"Could not connect to processing node backend server: {str(connection_error)}")
