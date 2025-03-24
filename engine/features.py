from playsound import playsound
import eel

# Function to play the assistant sound when the assistant is started
@eel.expose
def playAssistantSound():
    music_dir = "www/assets/audio/start_sound.wav"
    playsound(music_dir, True)