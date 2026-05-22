"""
Evaluation utilities for image quality assessment
"""

import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import numpy as np


class CLIPEvaluator:
    """CLIP-based image-text similarity evaluator"""
    
    def __init__(self, model_name="openai/clip-vit-base-patch32"):
        """Initialize CLIP model and processor"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained(model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_name)
    
    def compute_similarity(self, image, text):
        """
        Compute CLIP similarity score between image and text
        
        Args:
            image: PIL Image or path to image
            text: Text description
        
        Returns:
            float: Similarity score (0-1)
        """
        if isinstance(image, str):
            image = Image.open(image)
        
        # Process inputs
        inputs = self.processor(
            text=[text],
            images=image,
            return_tensors="pt",
            padding=True
        ).to(self.device)
        
        # Get embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            image_embeds = outputs.image_embeds
            text_embeds = outputs.text_embeds
            
            # Normalize embeddings
            image_embeds = image_embeds / image_embeds.norm(dim=-1, keepdim=True)
            text_embeds = text_embeds / text_embeds.norm(dim=-1, keepdim=True)
            
            # Compute cosine similarity
            similarity = (image_embeds @ text_embeds.T).item()
        
        return float(similarity)
    
    def batch_evaluate(self, images, texts):
        """
        Evaluate multiple image-text pairs
        
        Args:
            images: List of PIL Images or paths
            texts: List of text descriptions
        
        Returns:
            list: List of similarity scores
        """
        scores = []
        for image, text in zip(images, texts):
            score = self.compute_similarity(image, text)
            scores.append(score)
        return scores


def calculate_image_quality_metrics(image):
    """
    Calculate basic image quality metrics
    
    Args:
        image: PIL Image
    
    Returns:
        dict: Quality metrics
    """
    img_array = np.array(image)
    
    # Calculate metrics
    metrics = {
        "mean_brightness": float(np.mean(img_array)),
        "std_brightness": float(np.std(img_array)),
        "contrast": float(np.std(img_array) / (np.mean(img_array) + 1e-7)),
        "sharpness": float(np.std(np.gradient(img_array.astype(float))))
    }
    
    return metrics
