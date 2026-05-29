# Heavy ML logic: Whisper transcription, acoustic feature extraction, and image generation

import torch
import whisper
import librosa
import numpy as np
from diffusers import AutoPipelineForText2Image

from backend.config import (
    DEVICE,
    TORCH_DTYPE,
    IMAGE_MODEL_ID,
    NUM_INFERENCE_STEPS,
    GUIDANCE_SCALE,
    USE_SAFETENSORS
)
from backend.vocab import classify_telecom_category, build_prompt_from_category

_cached_models = {}


def load_ai_engines():
    """
    Initializes Whisper and image generation models using lazy loading.
    Models are loaded only once and reused for later requests.
    """
    global _cached_models

    if "whisper" not in _cached_models:
        print(f"Initializing Whisper Large-v3 Turbo ASR engine on {DEVICE}...")
        _cached_models["whisper"] = whisper.load_model("large-v3-turbo").to(DEVICE)

    if "image_model" not in _cached_models:
        print(f"Initializing image generation model: {IMAGE_MODEL_ID} on {DEVICE}...")

        model_kwargs = {
            "torch_dtype": TORCH_DTYPE,
            "use_safetensors": USE_SAFETENSORS
        }

        if DEVICE == "cuda" and USE_SAFETENSORS:
            model_kwargs["variant"] = "fp16"

        _cached_models["image_model"] = AutoPipelineForText2Image.from_pretrained(
            IMAGE_MODEL_ID,
            **model_kwargs
        ).to(DEVICE)

        _cached_models["image_model"].enable_attention_slicing()

        if DEVICE == "cuda":
            _cached_models["image_model"].enable_vae_slicing()

    return _cached_models


def compute_acoustic_diagnostics(audio_path: str) -> dict:
    """
    Calculates analytical audio features from the uploaded audio file.
    These values are saved in MongoDB.
    """
    y, sr = librosa.load(audio_path, sr=22050, mono=True)

    duration = float(librosa.get_duration(y=y, sr=sr))
    rms_energy = float(np.mean(librosa.feature.rms(y=y)))
    spectral_centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
    zero_crossing_rate = float(np.mean(librosa.feature.zero_crossing_rate(y)))
    spectral_rolloff = float(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)))

    mfcc_values = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc_values, axis=1)

    return {
        "duration_seconds": round(duration, 4),
        "rms_energy": round(rms_energy, 4),
        "spectral_centroid": round(spectral_centroid, 4),
        "brightness": round(spectral_centroid / sr, 4),
        "zero_crossing_rate": round(zero_crossing_rate, 4),
        "spectral_rolloff": round(spectral_rolloff, 4),
        "mfcc_mean": [round(float(value), 4) for value in mfcc_mean]
    }


def transcribe_audio(audio_path: str, whisper_model) -> str:
    """
    Converts speech audio into text using Whisper.
    """
    transcription_data = whisper_model.transcribe(audio_path, beam_size=5)
    transcript = transcription_data.get("text", "").strip()

    if not transcript:
        transcript = "telecommunication network service problem"

    return transcript


def execute_generative_synthesis(audio_path: str) -> tuple[str, dict, str, str, object]:
    """
    Runs the full AI pipeline:
    1. Load models
    2. Transcribe audio
    3. Extract acoustic features
    4. Classify telecom issue
    5. Build image prompt
    6. Generate image

    Returns:
        transcript, metrics, category, prompt, generated_image
    """
    engines = load_ai_engines()

    transcript = transcribe_audio(audio_path, engines["whisper"])

    metrics = compute_acoustic_diagnostics(audio_path)

    category = classify_telecom_category(transcript)

    optimized_prompt = build_prompt_from_category(category, transcript)

    with torch.inference_mode():
        generated_image = engines["image_model"](
            prompt=optimized_prompt,
            num_inference_steps=NUM_INFERENCE_STEPS,
            guidance_scale=GUIDANCE_SCALE
        ).images[0]

    return transcript, metrics, category, optimized_prompt, generated_image
