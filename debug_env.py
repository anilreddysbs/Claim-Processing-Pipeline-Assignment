import os
from pathlib import Path
from dotenv import load_dotenv

debug_info = []

cwd = Path.cwd()
debug_info.append(f"CWD: {cwd}")

env_path_1 = Path('.') / '.env'
env_path_2 = Path('..') / '.env'
env_path_3 = Path('c:/Users/USER/Desktop/task/.env')

debug_info.append(f"Checking {env_path_1.resolve()}: {env_path_1.exists()}")
debug_info.append(f"Checking {env_path_2.resolve()}: {env_path_2.exists()}")
debug_info.append(f"Checking {env_path_3.resolve()}: {env_path_3.exists()}")

# Try explicit load
if env_path_2.exists():
    load_dotenv(dotenv_path=env_path_2)

api_key = os.getenv("GOOGLE_API_KEY")
debug_info.append(f"GOOGLE_API_KEY found: {bool(api_key)}")
if api_key:
    debug_info.append(f"Key starts with: {api_key[:5]}...")

with open("debug_env.txt", "w") as f:
    f.write("\n".join(debug_info))
