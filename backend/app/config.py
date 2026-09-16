import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from backend directory if present
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

PORT = int(os.getenv("PORT", "8000"))
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# Default to llama-3.3-70b-versatile for Groq, or gemini-1.5-flash
default_model = "llama-3.3-70b-versatile" if GROQ_API_KEY else "gemini-1.5-flash"
LLM_MODEL = os.getenv("LLM_MODEL", default_model).strip()

# CORS origins split by comma
cors_raw = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
CORS_ORIGINS = [origin.strip() for origin in cors_raw.split(",") if origin.strip()]
