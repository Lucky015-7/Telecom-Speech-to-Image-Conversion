import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from backend.config import DEVICE, CLIP_MODEL

# Lazy load to optimize backend startup time
_processor = None
_model = None

def get_clip_resources():
    """Lazily instantiates and returns CLIP processor and model."""
    global _processor, _model
    if _processor is None or _model is None:
        _processor = CLIPProcessor.from_pretrained(CLIP_MODEL)
        _model = CLIPModel.from_pretrained(CLIP_MODEL).to(DEVICE)
    return _processor, _model

def calculate_clip_score(image_path: str, text_prompt: str) -> float:
    """
    Computes the visual-semantic similarity score between a saved image and a reference text prompt using CLIP.
    
    Parameters:
        image_path (str): Path to the generated image file.
        text_prompt (str): The descriptive query text to validate against.
        
    Returns:
        float: Similarity score between -1.0 and 1.0 (typically positive).
    """
    processor, model = get_clip_resources()
    
    # Load and preprocess image
    image = Image.open(image_path)
    inputs = processor(text=[text_prompt], images=image, return_tensors="pt", padding=True).to(DEVICE)
    
    with torch.no_grad():
        outputs = model(**inputs)
        # Normalize embeddings to calculate cosine similarity
        image_embeds = outputs.image_embeds / outputs.image_embeds.norm(p=2, dim=-1, keepdim=True)
        text_embeds = outputs.text_embeds / outputs.text_embeds.norm(p=2, dim=-1, keepdim=True)
        similarity = torch.matmul(image_embeds, text_embeds.t())
        
    return float(similarity.cpu().numpy()[0][0])
