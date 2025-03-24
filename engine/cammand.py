import pyttsx3
import speech_recognition as sr

def speak(text):
    engine=pyttsx3.init('sapi5')
    voices=engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    
    engine.setProperty('rate', 174)
    engine.say(text)
    engine.runAndWait()
    
def takecammand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold=1
        r.adjust_for_ambient_noise
        audio=r.listen(source,10,6)
    try:
        print("Recognizing...")
        query=r.recognize_google(audio,language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query.lower()
        
  
text= takecammand()  
speak(text)    