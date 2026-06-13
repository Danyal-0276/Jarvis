import os
import threading

import eel

from engine.features import *
from engine import documents
from engine.config import GEMINI_API_KEY

eel.init("www")

if GEMINI_API_KEY:
    threading.Thread(target=documents.build_index, daemon=True).start()

playAssistantSound()

os.system('start msedge.exe --app="http://localhost:8000/index.html"')
eel.start("index.html", mode=None, host="localhost", block=True)
