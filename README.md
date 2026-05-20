# Telecom Voice-to-Image Platform

A comprehensive, containerized application designed to process voice commands, extract key acoustic features, map them to a specialized telecommunications domain vocabulary, and generate corresponding descriptive images using Stable Diffusion, with similarity validation performed using CLIP scoring.

## Project Structure

```
telecom-voice-image/
│
├── .gitignore               # Tells Git which files/folders to ignore (e.g., venv, heavy images)
├── README.md                # Project documentation and setup instructions
├── requirements.txt         # List of Python dependencies to be installed via pip
├── Dockerfile               # Configuration for containerizing the app
├── docker-compose.yml       # Orchestrates frontend and backend containers
│
├── backend/                 # Backend API Service (FastAPI)
│   ├── __init__.py          # Marks this folder as a Python package
│   ├── main.py              # The primary FastAPI application and routing endpoints
│   ├── config.py            # Global variables, DEVICE selector (CUDA/CPU), and constants
│   ├── vocab.py             # Your 66-scene telecom domain vocabulary dictionary
│   └── utils/               # Helper modules for audio feature extraction and CLIP scoring
│       ├── __init__.py
│       ├── audio_utils.py   # Librosa feature extraction (RMS, Spectral Centroid, ZCR)
│       └── eval_utils.py    # CLIP similarity scoring implementation
│
├── frontend/                # Frontend Web Interface (Streamlit)
│   ├── __init__.py
│   └── app.py               # Main Streamlit application dashboard
│
└── data/                    # Local storage for data assets
    ├── inputs/              # Directory to place incoming voice files (e.g., voice3.mpeg)
    └── outputs/             # Directory where generated Stable Diffusion images are saved
```

## Quick Start
To get started:
1. Install dependencies: `pip install -r requirements.txt`
2. Start the FastAPI backend and Streamlit frontend.
