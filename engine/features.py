import hashlib
import os

import eel
from playsound import playsound

from engine import brain, documents
from engine.config import (
    ALLOWED_PATHS,
    EMAIL_CONFIRMATION,
    GEMINI_API_KEY,
    GMAIL_ADDRESS,
    STARTUP_PIN,
    VOICE_ENABLED,
)
from engine import email_service
from engine.voice import listen, speak


@eel.expose
def playAssistantSound():
    music_dir = "www/assets/audio/start_sound.wav"
    try:
        if os.path.exists(music_dir):
            playsound(music_dir, True)
    except Exception:
        pass


@eel.expose
def chat(message: str) -> dict:
    return brain.chat(message)


@eel.expose
def clear_chat() -> dict:
    brain.clear_history()
    email_service.clear_pending_email()
    return {"status": "done"}


@eel.expose
def listen_command() -> dict:
    return listen()


@eel.expose
def speak_text(text: str) -> dict:
    return speak(text)


@eel.expose
def confirm_email() -> dict:
    result = email_service.confirm_pending_email()
    return {"reply": result.get("message", "Done."), "status": result.get("status", "done")}


@eel.expose
def get_settings() -> dict:
    return {
        "gemini_configured": bool(GEMINI_API_KEY),
        "gmail_configured": bool(GMAIL_ADDRESS),
        "allowed_paths": [str(p) for p in ALLOWED_PATHS],
        "voice_enabled": VOICE_ENABLED,
        "email_confirmation": EMAIL_CONFIRMATION,
        "pin_enabled": bool(STARTUP_PIN),
        "document_count": documents.get_index_count() if GEMINI_API_KEY else 0,
    }


@eel.expose
def verify_pin(pin: str) -> dict:
    if not STARTUP_PIN:
        return {"status": "ok"}
    if hashlib.sha256(pin.encode()).hexdigest() == hashlib.sha256(STARTUP_PIN.encode()).hexdigest():
        return {"status": "ok"}
    return {"status": "error", "message": "Incorrect PIN"}


@eel.expose
def reindex_documents() -> dict:
    count = documents.build_index()
    return {"status": "done", "count": count}
