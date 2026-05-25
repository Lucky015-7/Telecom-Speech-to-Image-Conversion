import streamlit as st
import requests
import os

st.set_page_config(page_title="SLT Mobitel Generative Dashboard", layout="centered")

API_URL = "http://127.0.0.1:8000"

st.title("🎯 High-Accuracy Voice-to-Image Engine")
st.subheader("Telecom Customer Service Insights Console")
st.markdown("---")

uploaded_file = st.file_uploader(
    "Upload Customer Incident Recording",
    type=["mpeg", "mp3", "wav", "m4a", "webm", "ogg"]
)

if uploaded_file is not None:
    # Render native client playback widget
    st.audio(uploaded_file, format=uploaded_file.type)

    trigger_generation = st.button(
        "Generate Situational Image",
        type="primary",
        use_container_width=True
    )

    if trigger_generation:
        with st.spinner("Processing deep network pipeline stages... (This may take a moment to initialize)"):

            # Construct standard multipart form transfer envelope packages
            multipart_payload = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            try:
                response = requests.post(
                    f"{API_URL}/api/v1/process-audio",
                    files=multipart_payload
                )

                if response.status_code == 200:
                    payload = response.json()

                    # New backend returns data inside "result"
                    result = payload.get("result", {})

                    result_id = result.get("_id")
                    transcript = result.get("transcript", "No transcript available")
                    metrics = result.get("metrics", {})
                    category = result.get("category", "unknown")
                    prompt = result.get("prompt", "No prompt available")

                    st.success("Generative analysis sequence completed.")

                    # --- Structural Metric Blocks Layout ---
                    m1, m2, m3 = st.columns(3)

                    m1.metric(
                        "Signal RMS Loudness",
                        metrics.get("rms_energy", metrics.get("energy", 0))
                    )

                    m2.metric(
                        "Spectral Tonal Brightness",
                        metrics.get("brightness", 0)
                    )

                    m3.metric(
                        "Zero-Crossing Rate",
                        metrics.get("zero_crossing_rate", metrics.get("zcr", 0))
                    )

                    # --- Additional Backend Outputs ---
                    st.markdown("### 🧠 Telecom Issue Category")
                    st.info(category)

                    # --- Text Outputs Box Display ---
                    st.markdown("### 📋 Extracted Customer Complaint Transcript")
                    st.info(transcript)

                    st.markdown("### 📝 Generated Image Prompt")
                    st.info(prompt)

                    # --- Fetch and Render Final Generation Blob Asset ---
                    if result_id:
                        image_request_url = f"{API_URL}/api/v1/fetch-image/{result_id}"
                        image_data = requests.get(image_request_url)

                        if image_data.status_code == 200:
                            st.markdown("### 🖼️ High-Fidelity Synthesized Visual Output")
                            st.image(
                                image_data.content,
                                use_container_width=True,
                                caption="Generated Scene Map Model Frame"
                            )
                        else:
                            st.error("Target asset stream could not be safely piped from backend processing nodes.")
                    else:
                        st.error("Result ID was not returned by backend. Cannot fetch generated image.")

                else:
                    st.error(f"Backend Server Processing Error: {response.text}")

            except Exception as connection_error:
                st.error(f"Could not connect to processing node backend server: {str(connection_error)}")


st.markdown("---")

st.markdown("### 📂 Recent Backend Generation History")

if st.button("Load Recent Results"):
    try:
        history_response = requests.get(f"{API_URL}/api/v1/results")

        if history_response.status_code == 200:
            history_payload = history_response.json()
            results = history_payload.get("results", [])

            if len(results) == 0:
                st.info("No previous generation records found.")
            else:
                for item in results:
                    st.markdown("---")
                    st.write(f"**Result ID:** {item.get('_id')}")
                    st.write(f"**Original File:** {item.get('original_filename')}")
                    st.write(f"**Status:** {item.get('status')}")
                    st.write(f"**Category:** {item.get('category')}")
                    st.write(f"**Transcript:** {item.get('transcript')}")

                    item_id = item.get("_id")

                    if item_id:
                        image_url = f"{API_URL}/api/v1/fetch-image/{item_id}"
                        image_response = requests.get(image_url)

                        if image_response.status_code == 200:
                            st.image(
                                image_response.content,
                                use_container_width=True,
                                caption=f"Generated Image - {item.get('category')}"
                            )
        else:
            st.error(f"Could not load result history: {history_response.text}")

    except Exception as history_error:
        st.error(f"Could not connect to backend history endpoint: {str(history_error)}")


st.markdown("---")

st.markdown("### 📊 Backend Analytics")

if st.button("Load Category Analytics"):
    try:
        analytics_response = requests.get(f"{API_URL}/api/v1/analytics/categories")

        if analytics_response.status_code == 200:
            analytics_payload = analytics_response.json()
            analytics = analytics_payload.get("analytics", [])

            if len(analytics) == 0:
                st.info("No analytics data available yet.")
            else:
                st.table(analytics)
        else:
            st.error(f"Could not load analytics: {analytics_response.text}")

    except Exception as analytics_error:
        st.error(f"Could not connect to backend analytics endpoint: {str(analytics_error)}")