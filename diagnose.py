import os
import sys

# Add the project root to python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    print("Importing backend.utils...")
    from backend.utils import execute_generative_synthesis
    print("Import successful!")
except Exception as e:
    import traceback
    print("Import failed!")
    traceback.print_exc()
