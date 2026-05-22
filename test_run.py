import os
import sys
import traceback

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.utils import execute_generative_synthesis

audio_path = r"e:\Voice to image conversion\Telecom-Speech-to-Image-Conversion\data\inputs\voice3.mpeg"

try:
    print("Executing pipeline on voice3.mpeg...")
    transcript, metrics, image = execute_generative_synthesis(audio_path)
    print("Pipeline executed successfully!")
    print(f"Transcript: {transcript}")
    print(f"Metrics: {metrics}")
except Exception as e:
    print("Execution failed!")
    traceback.print_exc()
