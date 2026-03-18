from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[3]
load_dotenv(BASE_DIR / "backend" / ".env")

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
QUEUE_KEY = os.getenv("QUEUE_KEY", "subtitle_jobs")
STORAGE_DIR = (BASE_DIR / os.getenv("APP_STORAGE_DIR", "storage")).resolve()
JOBS_DIR = STORAGE_DIR / "jobs"
DOWNLOADS_DIR = STORAGE_DIR / "downloads"
TEMP_DIR = STORAGE_DIR / "temp"
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

for path in (STORAGE_DIR, JOBS_DIR, DOWNLOADS_DIR, TEMP_DIR):
    path.mkdir(parents=True, exist_ok=True)
