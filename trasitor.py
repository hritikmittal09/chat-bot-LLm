from transformers import pipeline
from spech import speak

translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-hi")
text = "I love reading long novels at night."
result = translator(text)

print("English:", text)
print("Hindi:", result[0]['translation_text'])
speak(result[0]['translation_text'])