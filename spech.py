import edge_tts
import asyncio
import os
import sys
import pyttsx3
def speak(text):
  
    engine = pyttsx3.init()

    # For Mac, If you face error related to "pyobjc" when running the `init()` method :
    # Install 9.0.1 version of pyobjc : "pip install pyobjc>=9.0.1"

    engine.say(f"{text}")
    engine.runAndWait()
    
if __name__ == "__main__":
    (speak("Hello, I am Roger. This is a test."))
    (speak("Hello, I am Roger. This is a test."))

