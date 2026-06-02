import os
import sys
import traceback

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.utils import execute_generative_synthesis

audio_path = r"e:\Voice to image conversion\Telecom-Speech-to-Image-Conversion\data\inputs\voice3.mpeg"

try:
    print("Executing pipeline on voice3.mpeg...")
    transcript, metrics, category, prompt, solutions, image = execute_generative_synthesis(audio_path)
    print("Pipeline executed successfully!")
    print(f"Transcript: {transcript}")
    print(f"Metrics: {metrics}")
    print(f"Category: {category}")
    print(f"Prompt: {prompt}")
    print(f"Solutions: {solutions}")
    
    # Save the output image to verify generation
    output_dir = os.path.join(os.path.dirname(__file__), "data", "outputs")
    os.makedirs(output_dir, exist_ok=True)
    image_path = os.path.join(output_dir, "test_run.png")
    image.save(image_path)
    print(f"Saved generated image to: {image_path}")
except Exception as e:
    print("Execution failed!")
    traceback.print_exc()
