"""
FastAPI Backend for Voice-to-Image Generation System
SLT Mobitel Research Project
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from transformers import ClapModel, ClapProcessor
from diffusers import StableDiffusionPipeline
from PIL import Image
import numpy as np
from pathlib import Path
import uuid
import logging
from datetime import datetime

from backend.config import *
from backend.utils.audio_utils import load_audio, extract_acoustic_features
from backend.utils.eval_utils import CLIPEvaluator
from backend.vocab import get_all_scenes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Voice-to-Image Generation API",
    description="SLT Mobitel Research - Convert voice to contextual images",
    version="3.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model storage
models = {}


def load_models():
    """Load all AI models into memory"""
    global models
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"Loading models on device: {device}")
    
    try:
        # Load Whisper for ASR
        logger.info("Loading Whisper model...")
        models['whisper_processor'] = WhisperProcessor.from_pretrained(MODELS['whisper'])
        models['whisper_model'] = WhisperForConditionalGeneration.from_pretrained(
            MODELS['whisper']
        ).to(device)
        
        # Load CLAP for audio-text matching
        logger.info("Loading CLAP model...")
        models['clap_processor'] = ClapProcessor.from_pretrained(MODELS['clap'])
        models['clap_model'] = ClapModel.from_pretrained(MODELS['clap']).to(device)
        
        # Load Stable Diffusion for image generation
        logger.info("Loading Stable Diffusion model...")
        models['sd_pipeline'] = StableDiffusionPipeline.from_pretrained(
            MODELS['stable_diffusion'],
            torch_dtype=torch.float16 if device == "cuda" else torch.float32
        ).to(device)
        
        if device == "cuda":
            models['sd_pipeline'].enable_attention_slicing()
        
        # Load CLIP for evaluation
        logger.info("Loading CLIP evaluator...")
        models['clip_evaluator'] = CLIPEvaluator(MODELS['clip'])
        
        # Pre-encode scene vocabulary with CLAP
        logger.info("Encoding scene vocabulary...")
        scenes = get_all_scenes()
        inputs = models['clap_processor'](
            text=scenes,
            return_tensors="pt",
            padding=True
        ).to(device)
        
        with torch.no_grad():
            models['scene_embeddings'] = models['clap_model'].get_text_features(**inputs)
            models['scene_embeddings'] = models['scene_embeddings'] / models['scene_embeddings'].norm(
                dim=-1, keepdim=True
            )
        
        models['scenes'] = scenes
        models['device'] = device
        
        logger.info("All models loaded successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")
        return False


@app.on_event("startup")
async def startup_event():
    """Load models on startup"""
    success = load_models()
    if not success:
        logger.warning("Models failed to load. API will have limited functionality.")


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Voice-to-Image Generation API",
        "version": "3.0",
        "organization": "SLT Mobitel Research",
        "status": "active",
        "models_loaded": len(models) > 0
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_loaded": len(models) > 0,
        "device": models.get('device', 'unknown'),
        "timestamp": datetime.now().isoformat()
    }


@app.post("/process/mode-a")
async def process_mode_a(file: UploadFile = File(...)):
    """
    Mode A: Audio-Direct Retrieval using CLAP
    Text-free audio understanding
    """
    if not models:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    try:
        # Save uploaded file
        file_id = str(uuid.uuid4())
        input_path = INPUT_DIR / f"{file_id}_{file.filename}"
        
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Load and process audio
        logger.info(f"Processing audio file: {file.filename}")
        audio, sr = load_audio(str(input_path), AUDIO_SAMPLE_RATE)
        
        # Extract acoustic features
        features = extract_acoustic_features(audio, sr)
        
        # Encode audio with CLAP
        inputs = models['clap_processor'](
            audios=audio,
            sampling_rate=sr,
            return_tensors="pt"
        ).to(models['device'])
        
        with torch.no_grad():
            audio_embeds = models['clap_model'].get_audio_features(**inputs)
            audio_embeds = audio_embeds / audio_embeds.norm(dim=-1, keepdim=True)
        
        # Compute similarity with scene vocabulary
        similarities = (audio_embeds @ models['scene_embeddings'].T).cpu().numpy()[0]
        top_k_indices = np.argsort(similarities)[-TOP_K_RETRIEVAL:][::-1]
        
        # Get best matching scene
        best_scene = models['scenes'][top_k_indices[0]]
        best_score = float(similarities[top_k_indices[0]])
        
        logger.info(f"Best match: {best_scene} (score: {best_score:.3f})")
        
        # Generate image using Stable Diffusion
        output_path = OUTPUT_DIR / f"{file_id}_mode_a.png"
        image = models['sd_pipeline'](
            prompt=best_scene,
            num_inference_steps=NUM_INFERENCE_STEPS,
            guidance_scale=GUIDANCE_SCALE
        ).images[0]
        
        image.save(output_path)
        
        # Evaluate with CLIP
        clip_score = models['clip_evaluator'].compute_similarity(image, best_scene)
        
        return {
            "success": True,
            "mode": "A",
            "file_id": file_id,
            "matched_scene": best_scene,
            "similarity_score": best_score,
            "clip_score": clip_score,
            "acoustic_features": features,
            "top_matches": [
                {
                    "scene": models['scenes'][idx],
                    "score": float(similarities[idx])
                }
                for idx in top_k_indices
            ],
            "output_image": str(output_path.name)
        }
        
    except Exception as e:
        logger.error(f"Error in Mode A processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/process/mode-b")
async def process_mode_b(file: UploadFile = File(...)):
    """
    Mode B: Speech Recognition + Text-Guided Generation
    Uses Whisper ASR + Stable Diffusion
    """
    if not models:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    try:
        # Save uploaded file
        file_id = str(uuid.uuid4())
        input_path = INPUT_DIR / f"{file_id}_{file.filename}"
        
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Load audio
        logger.info(f"Processing audio file: {file.filename}")
        audio, sr = load_audio(str(input_path), AUDIO_SAMPLE_RATE)
        
        # Extract acoustic features
        features = extract_acoustic_features(audio, sr)
        
        # Transcribe with Whisper
        inputs = models['whisper_processor'](
            audio,
            sampling_rate=sr,
            return_tensors="pt"
        ).to(models['device'])
        
        with torch.no_grad():
            predicted_ids = models['whisper_model'].generate(inputs.input_features)
            transcript = models['whisper_processor'].batch_decode(
                predicted_ids,
                skip_special_tokens=True
            )[0]
        
        logger.info(f"Transcript: {transcript}")
        
        # Generate image using transcript as prompt
        output_path = OUTPUT_DIR / f"{file_id}_mode_b.png"
        image = models['sd_pipeline'](
            prompt=transcript,
            num_inference_steps=NUM_INFERENCE_STEPS,
            guidance_scale=GUIDANCE_SCALE
        ).images[0]
        
        image.save(output_path)
        
        # Evaluate with CLIP
        clip_score = models['clip_evaluator'].compute_similarity(image, transcript)
        
        return {
            "success": True,
            "mode": "B",
            "file_id": file_id,
            "transcript": transcript,
            "clip_score": clip_score,
            "acoustic_features": features,
            "output_image": str(output_path.name)
        }
        
    except Exception as e:
        logger.error(f"Error in Mode B processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/image/{filename}")
async def get_image(filename: str):
    """Retrieve generated image"""
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(file_path)


@app.get("/scenes")
async def get_scenes():
    """Get all scene descriptions"""
    return {
        "total": len(models.get('scenes', [])),
        "scenes": models.get('scenes', [])
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
