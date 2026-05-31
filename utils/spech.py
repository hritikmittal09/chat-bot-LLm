import edge_tts
import asyncio
import os
import sys
import pyttsx3
def speak(text):
  
    engine = pyttsx3.init()

    # For Mac, If you face error related to "pyobjc" when running the `init()` method :
    # Install 9.0.1 version of pyobjc : "pip install pyobjc>=9.0.1"

    # Set to female voice
    voices = engine.getProperty('voices')
    # Select female voice (usually at index 1, but search for female voice)
    female_voice = None
    for voice in voices:
        if 'female' in voice.name.lower():
            female_voice = voice.id
            break
    # If no female voice found with 'female' in name, use second voice (usually female)
    if female_voice is None and len(voices) > 1:
        female_voice = voices[1].id
    
    if female_voice:
        engine.setProperty('voice', female_voice)
    
    engine.say(f"{text}")
    engine.runAndWait()
    
if __name__ == "__main__":
    (speak("Hello, I am Roger. This is a test."))
    (speak("Hello, I am Roger. This is a test."))

