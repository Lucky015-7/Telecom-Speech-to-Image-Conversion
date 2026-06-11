import os
import sys
import traceback

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.utils import execute_generative_synthesis

audio_path = r"e:\Voice to image conversion\Telecom-Speech-to-Image-Conversion\data\inputs\voice3.mpeg"

try:
    print("Executing pipeline on voice3.mpeg...")
    transcript, metrics, category, prompt, solutions, steps = execute_generative_synthesis(audio_path)
    print("Pipeline executed successfully!")
    print(f"Transcript: {transcript}")
    print(f"Metrics: {metrics}")
    print(f"Overall Category: {category}")
    print(f"Overall Prompt: {prompt}")
    print(f"Overall Solutions: {solutions}")
    print(f"Total Steps Generated: {len(steps)}")
    
    output_dir = os.path.join(os.path.dirname(__file__), "data", "outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    for idx, step in enumerate(steps):
        print(f"\n--- STEP {idx + 1} ---")
        print(f"Sentence: {step['sentence']}")
        print(f"Category: {step['category']}")
        print(f"Prompt: {step['prompt']}")
        print(f"Solutions: {step['solutions']}")
        
        image_path = os.path.join(output_dir, f"test_run_step_{idx}.png")
        step['image'].save(image_path)
        print(f"Saved step image to: {image_path}")
        
except Exception as e:
    print("Execution failed!")
    traceback.print_exc()
