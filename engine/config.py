import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


def _bool(value: str, default: bool = True) -> bool:
    if value is None or value == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
VOICE_ENABLED = _bool(os.getenv("VOICE_ENABLED"), True)
EMAIL_CONFIRMATION = _bool(os.getenv("EMAIL_CONFIRMATION"), True)
STARTUP_PIN = os.getenv("STARTUP_PIN", "")

ALLOWED_PATHS = [
    Path(p.strip()).resolve()
    for p in os.getenv("ALLOWED_PATHS", str(Path.home() / "Documents")).split(",")
    if p.strip()
]

MAX_FILE_SIZE_MB = 10
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md", ".csv"}
MAX_EMAILS_PER_SESSION = 10
