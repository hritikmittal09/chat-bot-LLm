import speech_recognition as sr

def user_voiceInput():
    recognizer = sr.Recognizer()

    # Threshold settings
    recognizer.pause_threshold = 1.0       
    recognizer.energy_threshold = 300     
    recognizer.dynamic_energy_threshold = True

    try:
        with sr.Microphone() as source:
            print("🎤 Say something...")

            
            recognizer.adjust_for_ambient_noise(source, duration=1)

            audio = recognizer.listen(
                source,
                timeout=2,              
            )

        try:
            text = recognizer.recognize_google(audio)

            print("✅ You said:", text)
            return text

        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
            return None

        except sr.RequestError as e:
            print(f"⚠️ API unavailable: {e}")
            return None

    except sr.WaitTimeoutError:
        print("⌛ No speech detected.")
        return None

    except Exception as e:
        print(f"⚠️ Error: {e}")
        return None


if __name__ == "__main__":
    user_voiceInput()
