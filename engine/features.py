from playsound import playsound

# Function to play the assistant sound when the assistant is started
def playAssistantSound():
    music_dir = "www/assets/audio/start_sound.mp3"
    playsound(music_dir, True)