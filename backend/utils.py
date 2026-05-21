# Heavy ML logic (Whisper transcription & SDXL image generation)
import torch
import whisper
import librosa
import numpy as np
from diffusers import AutoPipelineForText2Image
from backend.config import DEVICE, TORCH_DTYPE

_cached_models = {}


def load_ai_engines():
    """Initializes models into system memory using lazy loading."""
    global _cached_models
    if not _cached_models:
        print(f"Initializing Whisper Large-v3 Turbo ASR engine on {DEVICE}...")
        _cached_models['whisper'] = whisper.load_model(
            'large-v3-turbo').to(DEVICE)

        print(f"Initializing Stable Diffusion XL Pipeline on {DEVICE}...")
        _cached_models['sdxl'] = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=TORCH_DTYPE,
            variant="fp16" if DEVICE == "cuda" else None,
            use_safetensors=True
        ).to(DEVICE)

        # Apply VRAM memory optimization constraints if executing on a GPU cluster
        if DEVICE == "cuda":
            _cached_models['sdxl'].enable_attention_slicing()
            _cached_models['sdxl'].enable_vae_slicing()

    return _cached_models


def compute_acoustic_diagnostics(audio_path: str) -> dict:
    """Calculates underlying analytical audio wave vectors from a physical audio file."""
    y, sr = librosa.load(audio_path, sr=22050, mono=True)
    energy = float(np.mean(librosa.feature.rms(y=y)))
    brightness = float(
        np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))) / sr
    zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)))
    return {
        "energy": round(energy, 4),
        "brightness": round(brightness, 4),
        "zcr": round(zcr, 4)
    }


def execute_generative_synthesis(audio_path: str) -> tuple[str, dict, any]:
    """Runs high-fidelity transcription followed by optimized visual synthesis."""
    engines = load_ai_engines()

    # 1. Process Automatic Speech Recognition transcription
    transcription_data = engines['whisper'].transcribe(audio_path, beam_size=5)
    raw_transcript = transcription_data.get("text", "").strip()

    if not raw_transcript:
        raw_transcript = "telecommunication infrastructure line connection overview"

    # 2. Extract companion signal telemetry metrics
    telemetry_metrics = compute_acoustic_diagnostics(audio_path)

    # 3. Apply professional prompt design wrappers
    optimized_prompt = (
        f"A clear, crisp, professional documentary style photograph depicting: {raw_transcript}. "
        f"High fidelity, photorealistic, sharp focus, 8k resolution, detailed texture map."
    )

    # 4. Synthesize image via SDXL base framework
    with torch.inference_mode():
        generated_image = engines['sdxl'](
            prompt=optimized_prompt,
            num_inference_steps=30,
            guidance_scale=7.5
        ).images[0]

    return raw_transcript, telemetry_metrics, generated_image
