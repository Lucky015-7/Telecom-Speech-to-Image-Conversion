import os

os.environ["KMP_DUPLICATE_LIB_OK"] = os.getenv("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch
import whisper
import librosa
import numpy as np
from diffusers import AutoPipelineForText2Image

from backend.config import (
    DEVICE,
    TORCH_DTYPE,
    WHISPER_MODEL_NAME,
    IMAGE_MODEL_ID,
    NUM_INFERENCE_STEPS,
    GUIDANCE_SCALE,
    USE_SAFETENSORS
)

from backend.vocab import (
    classify_telecom_category,
    build_prompt_from_category,
    get_recommended_solutions
)

_cached_models = {}


def load_ai_engines():
    """
    Initializes Whisper ASR and Stable Diffusion image generation models.
    Models are loaded once and reused for later requests.
    """
    global _cached_models

    if "whisper" not in _cached_models:
        print(f"Initializing Whisper ASR engine: {WHISPER_MODEL_NAME} on {DEVICE}...")
        _cached_models["whisper"] = whisper.load_model(WHISPER_MODEL_NAME).to(DEVICE)

    if "sdxl" not in _cached_models:
        print(f"Initializing image generation model: {IMAGE_MODEL_ID} on {DEVICE}...")

        model_kwargs = {
            "torch_dtype": TORCH_DTYPE,
            "use_safetensors": USE_SAFETENSORS
        }

        if DEVICE == "cuda" and USE_SAFETENSORS:
            model_kwargs["variant"] = "fp16"

        _cached_models["sdxl"] = AutoPipelineForText2Image.from_pretrained(
            IMAGE_MODEL_ID,
            **model_kwargs
        ).to(DEVICE)

        _cached_models["sdxl"].enable_attention_slicing()

        if DEVICE == "cuda":
            _cached_models["sdxl"].enable_vae_slicing()

    return _cached_models


def compute_acoustic_diagnostics(audio_path: str) -> dict:
    """
    Calculates analytical audio features from the uploaded audio file.
    """
    y, sr = librosa.load(audio_path, sr=22050, mono=True)

    energy = float(np.mean(librosa.feature.rms(y=y)))
    brightness = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))) / sr
    zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)))

    return {
        "energy": round(energy, 4),
        "brightness": round(brightness, 4),
        "zcr": round(zcr, 4),

        # Extra names for frontend/backend compatibility
        "rms_energy": round(energy, 4),
        "zero_crossing_rate": round(zcr, 4)
    }


def transcribe_audio(audio_path: str, whisper_model) -> str:
    """
    Converts speech audio into text using Whisper.
    """
    transcription_data = whisper_model.transcribe(audio_path, beam_size=5)
    transcript = transcription_data.get("text", "").strip()

    if not transcript:
        transcript = "telecommunication infrastructure line connection overview"

    return transcript


def execute_generative_synthesis(audio_path: str) -> tuple[str, dict, str, str, list[str], object]:
    """
    Runs transcription, feature extraction, telecom classification,
    troubleshooting recommendation generation, prompt generation,
    and Stable Diffusion image generation.

    Returns:
        transcript, metrics, category, prompt, solutions, generated_image
    """
    engines = load_ai_engines()

    transcript = transcribe_audio(audio_path, engines["whisper"])

    metrics = compute_acoustic_diagnostics(audio_path)

    category = classify_telecom_category(transcript)

    category_prompt = build_prompt_from_category(category, transcript)

    solutions = get_recommended_solutions(category)

    optimized_prompt = (
        f"{category_prompt} "
        f"A clear, crisp, professional documentary style photograph depicting: {transcript}. "
        f"High fidelity, photorealistic, sharp focus, 8k resolution, detailed texture map."
    )

    with torch.inference_mode():
        generated_image = engines["sdxl"](
            prompt=optimized_prompt,
            num_inference_steps=NUM_INFERENCE_STEPS,
            guidance_scale=GUIDANCE_SCALE
        ).images[0]

    return transcript, metrics, category, optimized_prompt, solutions, generated_image