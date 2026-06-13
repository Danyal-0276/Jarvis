import pyttsx3
import speech_recognition as sr

from engine.config import VOICE_ENABLED

_engine = None


def _get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init("sapi5")
        voices = _engine.getProperty("voices")
        if len(voices) > 1:
            _engine.setProperty("voice", voices[1].id)
        _engine.setProperty("rate", 174)
    return _engine


def speak(text: str) -> dict:
    if not VOICE_ENABLED or not text:
        return {"status": "skipped"}
    try:
        engine = _get_engine()
        engine.say(text)
        engine.runAndWait()
        return {"status": "done"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def listen() -> dict:
    if not VOICE_ENABLED:
        return {"status": "error", "text": "", "message": "Voice is disabled in settings."}
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=10, phrase_time_limit=8)
        query = r.recognize_google(audio, language="en-in")
        return {"status": "done", "text": query}
    except sr.WaitTimeoutError:
        return {"status": "error", "text": "", "message": "No speech detected. Please try again."}
    except sr.UnknownValueError:
        return {"status": "error", "text": "", "message": "Could not understand. Please try again."}
    except Exception as e:
        return {"status": "error", "text": "", "message": str(e)}
