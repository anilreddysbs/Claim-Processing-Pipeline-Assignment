import os
import google.generativeai as genai
from dotenv import load_dotenv

from pathlib import Path

# Try identifying .env in current or parent directory
env_path = Path('.') / '.env'
if not env_path.exists():
    env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    with open("models.txt", "w") as f:
        f.write("Error: GOOGLE_API_KEY or GEMINI_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)

try:
    with open("models.txt", "w") as f:
        f.write("Listing available models...\n")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"{m.name}\n")
        f.write("Done listing models.\n")
except Exception as e:
    with open("models.txt", "a") as f:
        f.write(f"Error listing models: {e}\n")
