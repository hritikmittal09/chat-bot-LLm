from google import genai
from dotenv import load_dotenv
from google.genai import types
from functions.getFileInfo import get_files_info
from functions.get_file_content import get_file_content

import os

load_dotenv()

GAMINI_API_KEY = os.getenv("GAMNI_API-KEY")

print(get_file_content("Calculartor", "icalcular.py"))
prompt = input("enter prompt")
messages =[
     types.Content(role="user", parts=[types.Part(text=prompt)]),
       types.Content(
        role="system",
        parts=[types.Part(text="You are a helpful Python expert who explains code clearly.")]
    )
     
]

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=GAMINI_API_KEY)

response = client.models.generate_content(
model="gemini-2.5-flash-lite",
 contents= messages
)
print(response.text)