import os
import torch

# Auto-detect processing hardware layer
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Determine mathematical weight precision based on active architecture
TORCH_DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

# Central directory locations for processing assets
INPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "inputs"))
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "outputs"))

# Guarantee underlying sandbox file pathways exist safely
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)