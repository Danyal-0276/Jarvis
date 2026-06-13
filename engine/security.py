from pathlib import Path

from engine.config import ALLOWED_PATHS, MAX_FILE_SIZE_MB, SUPPORTED_EXTENSIONS


class SecurityError(Exception):
    pass


def is_path_allowed(path: Path) -> bool:
    resolved = path.resolve()
    for allowed in ALLOWED_PATHS:
        try:
            resolved.relative_to(allowed.resolve())
            return True
        except ValueError:
            continue
    return False


def validate_file_path(path: str | Path) -> Path:
    file_path = Path(path).resolve()
    if not is_path_allowed(file_path):
        raise SecurityError(f"Access denied: {file_path.name} is outside allowed folders.")
    if not file_path.exists():
        raise SecurityError(f"File not found: {file_path.name}")
    if not file_path.is_file():
        raise SecurityError(f"Not a file: {file_path.name}")
    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise SecurityError(f"Unsupported file type: {file_path.suffix}")
    size_mb = file_path.stat().st_size / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise SecurityError(f"File too large ({size_mb:.1f} MB). Max is {MAX_FILE_SIZE_MB} MB.")
    return file_path


def redact_secrets(text: str) -> str:
    import os
    from engine.config import GEMINI_API_KEY, GMAIL_APP_PASSWORD

    for secret in (GEMINI_API_KEY, GMAIL_APP_PASSWORD, os.getenv("STARTUP_PIN", "")):
        if secret and len(secret) > 4:
            text = text.replace(secret, "***")
    return text
