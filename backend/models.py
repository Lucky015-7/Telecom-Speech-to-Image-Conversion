from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class FeedbackRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class GenerationDocument(BaseModel):
    original_filename: str
    stored_audio_path: str
    output_image_path: Optional[str] = None
    transcript: Optional[str] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)
    category: Optional[str] = None
    prompt: Optional[str] = None

    # New backend feature field
    solutions: List[str] = Field(default_factory=list)

    status: str = "completed"
    feedback: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)