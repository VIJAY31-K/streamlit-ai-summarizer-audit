# check_env.py
import os
from dotenv import load_dotenv
load_dotenv()
print("GEMINI key found:", bool(os.getenv("GEMINI_API_KEY")))
