import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')
for v in voices:
    if "Ravi" in v.name:   # Or "HI-IN" in v.id
        engine.setProperty('voice', v.id)

engine.say("मुझे रात में लंबी कहानियाँ पढ़ना पसंद है।")
engine.runAndWait()
