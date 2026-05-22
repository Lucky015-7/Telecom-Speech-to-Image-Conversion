"""
Configuration settings for Voice-to-Image Generation System
SLT Mobitel Research Project
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "inputs"
OUTPUT_DIR = DATA_DIR / "outputs"

# Ensure directories exist
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Model configurations
MODELS = {
    "whisper": "openai/whisper-base",
    "clap": "laion/larger_clap_general",
    "clip": "openai/clip-vit-base-patch32",
    "stable_diffusion": "runwayml/stable-diffusion-v1-5"
}

# Audio settings
AUDIO_SAMPLE_RATE = 48000
SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".mpeg", ".m4a", ".flac"]

# Generation settings
TOP_K_RETRIEVAL = 5
IMAGE_SIZE = (512, 512)
NUM_INFERENCE_STEPS = 50
GUIDANCE_SCALE = 7.5

# API settings
API_HOST = "0.0.0.0"
API_PORT = 8000
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB

# Scene vocabulary categories
SCENE_CATEGORIES = {
    "communication_infrastructure": [
        "Damaged communication tower with engineers working",
        "Telecommunications tower against blue sky",
        "Engineers repairing cellular antennas on tower",
        "Fiber optic cable installation in progress",
        "Underground cable laying by technicians",
        "Satellite dish installation on building rooftop",
        "Network infrastructure maintenance crew",
        "Telecommunications equipment room with racks",
        "Cell tower with multiple antenna arrays",
        "Technician climbing communication tower"
    ],
    "router_home_network": [
        "WiFi router with blinking orange warning light",
        "Modern router with green status LEDs",
        "Technician configuring home router setup",
        "Server room with network equipment racks",
        "Home office desk with router and modem",
        "Network switch with multiple ethernet cables",
        "Router installation in customer home",
        "Speed test running on laptop screen",
        "Mesh WiFi system in modern home",
        "Network diagnostic tools on computer screen"
    ],
    "internet_devices": [
        "Laptop showing browser connection error page",
        "Mobile phone displaying full WiFi signal strength"
    ],
    "television_services": [
        "Television screen showing no signal message",
        "Set-top box with connected cables",
        "Cable TV control room with monitors",
        "Technician installing satellite dish",
        "TV remote control and set-top box",
        "Digital TV signal quality test screen",
        "IPTV streaming interface on smart TV",
        "Broadcast equipment in control center"
    ],
    "customer_service": [
        "Modern call center with rows of service agents",
        "Customer service representative with headset",
        "Service van parked outside residential house",
        "Field technician visiting customer home",
        "Help desk agent assisting customer",
        "Technical support team in office",
        "Mobile service unit in neighborhood",
        "Customer meeting with service representative"
    ],
    "faults_outages": [
        "Network outage map with red affected areas",
        "Storm damage to telecommunications poles",
        "Power outage affecting city street at night",
        "Damaged cables after severe weather",
        "Emergency repair crew working at night",
        "Service interruption notification screen",
        "Broken utility pole with hanging wires",
        "Flooded telecommunications equipment room"
    ],
    "billing_plans": [
        "Digital invoice displayed on computer screen",
        "Service plan comparison chart",
        "Contract document being signed",
        "Payment terminal for bill payment",
        "Mobile app showing billing details",
        "Customer reviewing service agreement"
    ],
    "network_data": [
        "Global internet connectivity map visualization",
        "Modern data center with server racks",
        "Video streaming buffering symbol on screen",
        "Network traffic monitoring dashboard",
        "Cloud computing infrastructure diagram",
        "High-speed fiber optic network cables",
        "Network operations center with displays",
        "Internet speed test results on screen"
    ],
    "environment_context": [
        "Suburban neighborhood with utility cables",
        "Person working from home office setup",
        "Network switch with illuminated LEDs",
        "Urban area with telecommunications infrastructure",
        "Residential area with cable connections",
        "Home internet setup in living room"
    ]
}

# Flatten scene vocabulary
SCENE_VOCABULARY = []
for category, scenes in SCENE_CATEGORIES.items():
    SCENE_VOCABULARY.extend(scenes)

# Processing modes
PROCESSING_MODES = {
    "A": "Audio-Direct Retrieval (CLAP)",
    "B": "Speech Recognition + Text-Guided Generation (Whisper + SD)"
}
