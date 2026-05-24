import os
import torch
from dotenv import load_dotenv

load_dotenv()

# Auto-detect processing hardware layer
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Determine mathematical weight precision based on active architecture
TORCH_DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

# Base project directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Central directory locations for processing assets
INPUT_DIR = os.path.join(BASE_DIR, "data", "inputs")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "outputs")

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "slt_voice_to_image_db")

# Image generation configuration
IMAGE_MODEL_ID = os.getenv("IMAGE_MODEL_ID", "segmind/tiny-sd")
NUM_INFERENCE_STEPS = int(os.getenv("NUM_INFERENCE_STEPS", "8"))
GUIDANCE_SCALE = float(os.getenv("GUIDANCE_SCALE", "6.0"))
USE_SAFETENSORS = os.getenv("USE_SAFETENSORS", "false").lower() == "true"

# Audio upload validation
ALLOWED_AUDIO_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".mpeg",
    ".mp4",
    ".m4a",
    ".webm",
    ".ogg"
}

MAX_AUDIO_FILE_SIZE_MB = 25
MAX_AUDIO_FILE_SIZE_BYTES = MAX_AUDIO_FILE_SIZE_MB * 1024 * 1024