import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from backend.config import INPUT_DIR, OUTPUT_DIR
from backend.utils import execute_generative_synthesis

app = FastAPI(title="SLT Mobitel Voice-to-Image Generation Service Architecture")

@app.post("/api/v1/process-audio")
async def process_audio_endpoint(file: UploadFile = File(...)):
    """Receives binary audio streams, stages them locally, and runs generation."""
    staged_audio_path = os.path.join(INPUT_DIR, file.filename)
    
    # Save the incoming file stream onto local storage
    with open(staged_audio_path, "wb") as buffer:
        buffer.write(await file.read())
        
    try:
        # Run execution pipeline layers
        transcript, metrics, image_object = execute_generative_synthesis(staged_audio_path)
        
        # Save output tracking assets
        output_filename = f"prod_{os.path.splitext(file.filename)[0]}.png"
        staged_image_path = os.path.join(OUTPUT_DIR, output_filename)
        image_object.save(staged_image_path)
        
        return {
            "status": "success",
            "transcript": transcript,
            "metrics": metrics,
            "image_path": staged_image_path
        }
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

@app.get("/api/v1/fetch-image")
def fetch_image_endpoint(path: str):
    """Safely retrieves generated target assets based on data paths."""
    if os.path.exists(path):
        return FileResponse(path, media_type="image/png")
    raise HTTPException(status_code=404, detail="Requested generation asset path missing.")