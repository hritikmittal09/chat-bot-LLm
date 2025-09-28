import speech_recognition as sr

def user_voiceInput():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("✅ You said:", text)
        return text

    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return None
    except sr.RequestError:
        print("⚠️ API unavailable or internet issue.")
        return None

if __name__ == "__main__":
    user_voiceInput()
