import os 
import eel
from engine.features import *
eel.init("www") # This will look for the index.html file in the www folder

playAssistantSound()

os.system('start msedge.exe --app="http://localhost:8000/index.html"')
eel.start('index.html', mode=None,host='localhost',block=True)   # This will open the browser window with the given size
